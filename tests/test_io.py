"""Tests for I/O utilities in brc_schema.util.io"""

import json
import tempfile
import yaml
from pathlib import Path

import pytest

from brc_schema.util.io import dump_output, sanitize_for_yaml, remove_none_values


class TestSanitizeForYaml:
    """Test the sanitize_for_yaml function."""

    def test_primitives_unchanged(self):
        """Test that primitive types pass through unchanged."""
        assert sanitize_for_yaml(None) is None
        assert sanitize_for_yaml("test") == "test"
        assert sanitize_for_yaml(42) == 42
        assert sanitize_for_yaml(3.14) == 3.14
        assert sanitize_for_yaml(True) is True
        assert sanitize_for_yaml(False) is False

    def test_lists_sanitized_recursively(self):
        """Test that lists are recursively sanitized."""
        input_data = [1, "test", [2, 3], {"key": "value"}]
        result = sanitize_for_yaml(input_data)
        assert result == [1, "test", [2, 3], {"key": "value"}]

    def test_dicts_sanitized_recursively(self):
        """Test that dictionaries are recursively sanitized."""
        input_data = {
            "string": "value",
            "number": 42,
            "nested": {"inner": "data"},
            "list": [1, 2, 3]
        }
        result = sanitize_for_yaml(input_data)
        assert result == input_data

    def test_dynamic_objects_replaced(self, caplog):
        """Test that dynamic objects are replaced with empty strings."""

        class MockDynamicObject:
            def __repr__(self):
                return '<linkml_map.utils.dynamic_object.Person object at 0x7fca200bb620>'

        test_data = {
            "valid_field": "keep this",
            "dynamic_object": MockDynamicObject(),
            "list_with_objects": [1, MockDynamicObject(), "keep"]
        }

        result = sanitize_for_yaml(test_data)

        expected = {
            "valid_field": "keep this",
            "dynamic_object": "",
            "list_with_objects": [1, "", "keep"]
        }

        assert result == expected
        # Check that warnings were logged
        assert "Encountered non-serializable object" in caplog.text
        assert "MockDynamicObject" in caplog.text

    def test_nested_dynamic_objects(self, caplog):
        """Test sanitization of nested structures with dynamic objects."""

        class MockObject:
            def __repr__(self):
                return '<linkml_map.utils.dynamic_object.Organization object at 0x123456>'

        nested_data = {
            "level1": {
                "level2": {
                    "object": MockObject(),
                    "valid": "data"
                },
                "array": [MockObject(), "valid"]
            }
        }

        result = sanitize_for_yaml(nested_data)

        expected = {
            "level1": {
                "level2": {
                    "object": "",
                    "valid": "data"
                },
                "array": ["", "valid"]
            }
        }

        assert result == expected
        assert "root.level1.level2.object" in caplog.text
        assert "root.level1.array[0]" in caplog.text

    def test_custom_objects_with_dict(self, caplog):
        """Test that custom objects with __dict__ are replaced."""

        class CustomObject:
            def __init__(self):
                self.attr = "value"

            def __repr__(self):
                return "CustomObject(attr='value')"

        test_data = {"custom": CustomObject()}
        result = sanitize_for_yaml(test_data)

        assert result == {"custom": ""}
        assert "CustomObject" in caplog.text


class TestDumpOutput:
    """Test the dump_output function with various formats."""

    def test_yaml_output_to_file(self):
        """Test YAML output to file."""
        test_data = {"datasets": [{"name": "test", "value": 42}]}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = f.name

        try:
            dump_output(test_data, "yaml", temp_path)

            # Verify file was created and contains valid YAML
            with open(temp_path, 'r') as f:
                loaded_data = yaml.safe_load(f)

            assert loaded_data == test_data
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_json_output_to_file(self):
        """Test JSON output to file."""
        test_data = {"datasets": [{"name": "test", "value": 42}]}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            dump_output(test_data, "json", temp_path)

            # Verify file was created and contains valid JSON
            with open(temp_path, 'r') as f:
                loaded_data = json.load(f)

            # LinkML JSON dumper adds @type metadata, so verify core data is preserved
            assert loaded_data["datasets"] == test_data["datasets"]
            # Verify it's valid JSON with LinkML metadata
            assert "@type" in loaded_data
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_yaml_output_to_stdout(self, capsys):
        """Test YAML output to stdout."""
        test_data = {"key": "value"}

        dump_output(test_data, "yaml", None)

        captured = capsys.readouterr()
        loaded_data = yaml.safe_load(captured.out)
        assert loaded_data == test_data

    def test_json_output_to_stdout(self, capsys):
        """Test JSON output to stdout."""
        test_data = {"key": "value"}

        dump_output(test_data, "json", None)

        captured = capsys.readouterr()
        loaded_data = json.loads(captured.out)
        # LinkML JSON dumper adds @type metadata, so verify core data is preserved
        assert loaded_data["key"] == test_data["key"]
        assert "@type" in loaded_data

    def test_str_output_with_string_input(self, capsys):
        """Test string output with string input."""
        test_string = "Hello, World!"

        dump_output(test_string, "str", None)

        captured = capsys.readouterr()
        assert captured.out == test_string

    def test_str_output_with_non_string_input(self, capsys):
        """Test string output with non-string input."""
        test_data = {"key": "value"}

        dump_output(test_data, "str", None)

        captured = capsys.readouterr()
        assert captured.out == str(test_data)

    def test_default_format_with_string(self, capsys):
        """Test default format (None) with string input."""
        test_string = "Test string"

        dump_output(test_string, None, None)

        captured = capsys.readouterr()
        assert captured.out == test_string

    def test_default_format_with_non_string(self, capsys):
        """Test default format (None) with non-string input."""
        test_data = [1, 2, 3]

        dump_output(test_data, None, None)

        captured = capsys.readouterr()
        assert captured.out == str(test_data)

    def test_sanitization_in_yaml_output(self, caplog):
        """Test that YAML output sanitizes dynamic objects."""

        class MockDynamicObject:
            def __repr__(self):
                return '<linkml_map.utils.dynamic_object.Person object at 0x123>'

        test_data = {
            "datasets": [{
                "name": "test",
                "creator": MockDynamicObject(),
                "value": 42
            }]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = f.name

        try:
            dump_output(test_data, "yaml", temp_path)

            # Verify sanitization occurred
            assert "Encountered non-serializable object" in caplog.text

            # Verify output is valid YAML with sanitized data
            with open(temp_path, 'r') as f:
                loaded_data = yaml.safe_load(f)

            expected = {
                "datasets": [{
                    "name": "test",
                    "creator": "",  # Sanitized
                    "value": 42
                }]
            }
            assert loaded_data == expected
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_sanitization_in_json_output(self, caplog):
        """Test that JSON output sanitizes dynamic objects."""

        class MockDynamicObject:
            def __repr__(self):
                return '<linkml_map.utils.dynamic_object.Organization object at 0x456>'

        test_data = {
            "datasets": [{
                "name": "test",
                "funding": [MockDynamicObject()],
                "value": 42
            }]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            dump_output(test_data, "json", temp_path)

            # Verify sanitization occurred
            assert "Encountered non-serializable object" in caplog.text

            # Verify output is valid JSON with sanitized data
            with open(temp_path, 'r') as f:
                loaded_data = json.load(f)

            # Verify the core data structure with sanitized objects
            # LinkML JSON dumper adds @type metadata, so check the actual data
            assert len(loaded_data["datasets"]) == 1
            dataset = loaded_data["datasets"][0]
            assert dataset["name"] == "test"
            assert dataset["funding"] == [""]  # Sanitized
            assert dataset["value"] == 42
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_unsupported_format_raises_error(self):
        """Test that unsupported formats raise NotImplementedError."""
        with pytest.raises(NotImplementedError, match="Output format xml is not supported"):
            dump_output({"test": "data"}, "xml", None)

    def test_unsupported_format_conditions(self):
        """Test edge cases in format handling."""
        # Test that empty string format raises ValueError (per the actual logic)
        test_data = {"key": "value"}

        with pytest.raises(ValueError, match="No output to be printed"):
            # Empty string format is not None and not a supported format
            # This should trigger the final else clause
            dump_output(test_data, "", None)


class TestIntegration:
    """Integration tests combining sanitization and output formatting."""

    def test_complex_data_structure_yaml_and_json_equivalent(self):
        """Test that complex data produces equivalent YAML and JSON output."""

        # Create complex test data
        test_data = {
            "datasets": [
                {
                    "brc": "GLBRC",
                    "title": "Test Dataset",
                    "creator": [
                        {
                            "name": "John Doe",
                            "email": "john@example.com",
                            "primaryContact": True
                        }
                    ],
                    "funding": [
                        {
                            "fundingOrganization": {
                                "organizationName": "DOE"
                            },
                            "awardNumber": "DE-123456"
                        }
                    ],
                    "active": True,
                    "has_related_ids": ["BIOPROJECT:123"]
                }
            ]
        }

        yaml_path = None
        json_path = None

        try:
            # Write as YAML
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                yaml_path = f.name
            dump_output(test_data, "yaml", yaml_path)

            # Write as JSON
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json_path = f.name
            dump_output(test_data, "json", json_path)

            # Load both and compare
            with open(yaml_path, 'r') as f:
                yaml_data = yaml.safe_load(f)

            with open(json_path, 'r') as f:
                json_data = json.load(f)

            # YAML data should match input exactly
            assert yaml_data == test_data

            # JSON data has LinkML metadata but core structure should match
            assert json_data["datasets"] == test_data["datasets"]
            assert "@type" in json_data

        finally:
            if yaml_path:
                Path(yaml_path).unlink(missing_ok=True)
            if json_path:
                Path(json_path).unlink(missing_ok=True)

    def test_real_world_scenario_with_mixed_objects(self, caplog):
        """Test a real-world scenario with mixed valid and invalid objects."""

        class PersonObject:
            def __repr__(self):
                return '<linkml_map.utils.dynamic_object.Person object at 0x789>'

        class OrganizationObject:
            def __repr__(self):
                return '<linkml_map.utils.dynamic_object.Organization object at 0xabc>'

        # Simulate transformation output with some dynamic objects
        mixed_data = {
            "datasets": [
                {
                    "brc": "CBI",
                    "title": "Research Dataset",
                    "creator": PersonObject(),  # Should be sanitized
                    # Should be sanitized
                    "contributors": [PersonObject(), PersonObject()],
                    "funding": [
                        {
                            "fundingOrganization": OrganizationObject(),  # Should be sanitized
                            "awardNumber": "SC0018420"
                        }
                    ],
                    "description": "Valid text field",  # Should remain
                    "active": True,  # Should remain
                    "dataset_url": "https://example.com"  # Should remain
                }
            ]
        }

        json_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json_path = f.name

            dump_output(mixed_data, "json", json_path)

            # Verify sanitization warnings
            log_text = caplog.text
            assert "root.datasets[0].creator" in log_text
            assert "root.datasets[0].contributors[0]" in log_text
            assert "root.datasets[0].funding[0].fundingOrganization" in log_text

            # Verify output is valid JSON with sanitized objects
            with open(json_path, 'r') as f:
                result = json.load(f)

            dataset = result["datasets"][0]
            assert dataset["creator"] == ""
            assert dataset["contributors"] == ["", ""]
            assert dataset["funding"][0]["fundingOrganization"] == ""

            # Verify valid fields are preserved
            assert dataset["brc"] == "CBI"
            assert dataset["title"] == "Research Dataset"
            assert dataset["description"] == "Valid text field"
            assert dataset["active"] is True
            assert dataset["dataset_url"] == "https://example.com"
            assert dataset["funding"][0]["awardNumber"] == "SC0018420"

        finally:
            if json_path:
                Path(json_path).unlink(missing_ok=True)


class TestRemoveNoneValues:
    """Test the remove_none_values function."""

    def test_primitives_unchanged(self):
        """Test that primitive types pass through unchanged."""
        assert remove_none_values("test") == "test"
        assert remove_none_values(42) == 42
        assert remove_none_values(3.14) == 3.14
        assert remove_none_values(True) is True
        assert remove_none_values(False) is False
        assert remove_none_values(None) is None

    def test_dict_none_values_removed(self):
        """Test that None values are removed from dictionaries."""
        input_data = {
            "keep_string": "value",
            "keep_number": 42,
            "remove_none": None,
            "keep_false": False,
            "keep_empty_list": [],
            "remove_none_nested": {
                "nested_keep": "value",
                "nested_remove": None
            }
        }

        expected = {
            "keep_string": "value",
            "keep_number": 42,
            "keep_false": False,
            "keep_empty_list": [],
            "remove_none_nested": {
                "nested_keep": "value"
            }
        }

        result = remove_none_values(input_data)
        assert result == expected

    def test_list_none_values_removed(self):
        """Test that None values are removed from lists."""
        input_data = ["keep", None, 42, None, "also keep", [None, "nested"]]
        expected = ["keep", 42, "also keep", ["nested"]]

        result = remove_none_values(input_data)
        assert result == expected

    def test_nested_structures(self):
        """Test complex nested structures with None values."""
        input_data = {
            "datasets": [
                {
                    "title": "Dataset 1",
                    "description": None,
                    "keywords": ["keyword1", "keyword2"],
                    "has_related_ids": None,
                    "creator": None
                },
                {
                    "title": "Dataset 2",
                    "description": "Valid description",
                    "keywords": None,
                    "has_related_ids": ["BIOPROJECT:123"],
                    "metadata": {
                        "valid_field": "keep",
                        "empty_field": None
                    }
                }
            ],
            "empty_field": None
        }

        expected = {
            "datasets": [
                {
                    "title": "Dataset 1",
                    "keywords": ["keyword1", "keyword2"]
                },
                {
                    "title": "Dataset 2",
                    "description": "Valid description",
                    "has_related_ids": ["BIOPROJECT:123"],
                    "metadata": {
                        "valid_field": "keep"
                    }
                }
            ]
        }

        result = remove_none_values(input_data)
        assert result == expected

    def test_empty_dict_preserved(self):
        """Test that empty dictionaries are preserved (not None)."""
        input_data = {
            "empty_dict": {},
            "none_field": None
        }

        expected = {
            "empty_dict": {}
        }

        result = remove_none_values(input_data)
        assert result == expected
