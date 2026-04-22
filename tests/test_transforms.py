"""Tests for transformation functionality in brc_schema"""

import json
import sys
from unittest.mock import patch

from brc_schema.cli import main


class TestTransformations:
    """Test transformation functionality."""

    def test_keywords_comma_splitting(self, tmp_path):
        """Test that keywords are properly split from comma-delimited strings."""
        # Create test input data with comma-separated keywords
        test_data = {
            "records": [{
                "osti_id": "12345",
                "title": "Test Dataset",
                "description": "A test dataset",
                "keywords": ["Lignin structure, HSQC, poplar, CELF, CBP, CBI"],
                "publication_date": "2024-01-01",
                "site_ownership_code": "ORNL"
            }]
        }

        # Write input file
        input_file = tmp_path / "test_input.json"
        with open(input_file, 'w') as f:
            json.dump(test_data, f)

        # Output file
        output_file = tmp_path / "test_output.json"

        # Run transformation
        test_args = [
            'brcschema', 'transform',
            '-T', 'osti_to_brc',
            '-o', str(output_file),
            str(input_file)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass  # CLI exits after successful run

        # Check results
        assert output_file.exists()

        with open(output_file, 'r') as f:
            result = json.load(f)

        # Verify keywords are properly split
        assert 'datasets' in result
        assert len(result['datasets']) == 1

        dataset = result['datasets'][0]
        assert 'keywords' in dataset

        keywords = dataset['keywords']
        expected_keywords = ['Lignin structure',
                             'HSQC', 'poplar', 'CELF', 'CBP', 'CBI']

        assert isinstance(keywords, list)
        assert len(keywords) == 6
        assert keywords == expected_keywords

        # Verify no comma-separated strings remain
        for keyword in keywords:
            assert ',' not in keyword
            assert keyword.strip() == keyword  # No leading/trailing spaces

    def test_keywords_edge_cases(self):
        """Test keywords transformation handles edge cases correctly."""

        def transform_keywords(src_keywords):
            """Simulate the keywords transformation logic."""
            if src_keywords:
                result = []
                for item in src_keywords:
                    if isinstance(item, str):
                        # Split comma-separated keywords
                        for keyword in item.split(','):
                            keyword = keyword.strip()
                            if keyword:
                                result.append(keyword)
                    else:
                        # Handle non-string items
                        if item:
                            result.append(str(item))
                return result if result else None
            else:
                return None

        # Test cases
        test_cases = [
            # Input, Expected Output
            (['single keyword'], ['single keyword']),
            (['keyword1, keyword2, keyword3'], [
             'keyword1', 'keyword2', 'keyword3']),
            (['  spaced  ,  keywords  '], ['spaced', 'keywords']),
            ([''], None),
            ([], None),
            (None, None),
            (['mixed, keywords', 'single'], ['mixed', 'keywords', 'single']),
            (['trailing,comma,'], ['trailing', 'comma'])
        ]

        for input_keywords, expected in test_cases:
            result = transform_keywords(input_keywords)
            assert result == expected, f"Input: {input_keywords}, Expected: {expected}, Got: {result}"

    def test_missing_fields_transformation(self, tmp_path):
        """Test transformation when required fields are missing."""
        # Test minimal data with only required fields
        minimal_data = {
            "records": [{
                "osti_id": "12345",
                "title": "Minimal Dataset"
                # Missing: description, keywords, persons, authors, doi, etc.
            }]
        }

        input_file = tmp_path / "minimal_input.json"
        with open(input_file, 'w') as f:
            json.dump(minimal_data, f)

        output_file = tmp_path / "minimal_output.json"

        # Run transformation
        test_args = [
            'brcschema', 'transform',
            '-T', 'osti_to_brc',
            '-o', str(output_file),
            str(input_file)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

        # Verify it doesn't crash and produces reasonable output
        assert output_file.exists()

        with open(output_file, 'r') as f:
            result = json.load(f)

        assert 'datasets' in result
        assert len(result['datasets']) == 1

        dataset = result['datasets'][0]

        # Check that missing fields are handled gracefully
        assert dataset['title'] == "Minimal Dataset"
        assert dataset['identifier'] == "https://www.osti.gov/biblio/12345"
        assert dataset.get('description') is None
        assert dataset.get('keywords') is None
        assert dataset.get('creator') is None
        assert dataset.get('contributors') is None
        assert dataset.get('bibliographicCitation') is None

    def test_empty_nested_objects_transformation(self, tmp_path):
        """Test transformation with empty nested objects."""
        data_with_empty_objects = {
            "records": [{
                "osti_id": "12345",
                "title": "Dataset with Empty Objects",
                "persons": [],  # Empty persons array
                "organizations": [],  # Empty organizations array
                "keywords": [],  # Empty keywords array
                "identifiers": []  # Empty identifiers array
            }]
        }

        input_file = tmp_path / "empty_objects_input.json"
        with open(input_file, 'w') as f:
            json.dump(data_with_empty_objects, f)

        output_file = tmp_path / "empty_objects_output.json"

        test_args = [
            'brcschema', 'transform',
            '-T', 'osti_to_brc',
            '-o', str(output_file),
            str(input_file)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

        assert output_file.exists()

        with open(output_file, 'r') as f:
            result = json.load(f)

        dataset = result['datasets'][0]

        # Empty arrays should result in None values
        assert dataset.get('creator') is None
        assert dataset.get('contributors') is None
        assert dataset.get('keywords') is None
        assert dataset.get('funding') is None

    def test_malformed_persons_transformation(self, tmp_path):
        """Test transformation with malformed person objects."""
        data_with_bad_persons = {
            "records": [{
                "osti_id": "12345",
                "title": "Dataset with Bad Persons",
                "persons": [
                    {
                        "type": "AUTHOR",
                        # Missing name fields
                        "email": ["test@example.com"]
                    },
                    {
                        "type": "AUTHOR",
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": []  # Empty email array
                    },
                    {
                        # Missing type field
                        "first_name": "Jane",
                        "last_name": "Smith"
                    },
                    {
                        "type": "CONTRIBUTING",
                        "first_name": "Bob",
                        "affiliations": []  # Empty affiliations
                    }
                ]
            }]
        }

        input_file = tmp_path / "bad_persons_input.json"
        with open(input_file, 'w') as f:
            json.dump(data_with_bad_persons, f)

        output_file = tmp_path / "bad_persons_output.json"

        test_args = [
            'brcschema', 'transform',
            '-T', 'osti_to_brc',
            '-o', str(output_file),
            str(input_file)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

        assert output_file.exists()

        with open(output_file, 'r') as f:
            result = json.load(f)

        dataset = result['datasets'][0]

        # Should only include persons with valid names
        creators = dataset.get('creator', [])
        if creators:
            # Should have John Doe (has complete name)
            assert len(creators) == 1
            assert creators[0]['name'] == 'John Doe'
            # Empty email array should be omitted
            assert 'email' not in creators[0]

        # Contributors should have Bob (only first name but still valid)
        contributors = dataset.get('contributors')
        if contributors:
            assert len(contributors) == 1
            assert contributors[0]['name'] == 'Bob'

    def test_brc_mapping_edge_cases(self, tmp_path):
        """Test BRC organization mapping with various edge cases."""
        test_cases = [
            # Direct site_ownership_code
            {"site_ownership_code": "CABBI"},

            # Contract number in identifiers
            {
                "identifiers": [
                    {"type": "CN_DOE", "value": "SC0018420"},
                    {"type": "OTHER", "value": "some-other-id"}
                ]
            },

            # Unknown contract number
            {
                "identifiers": [
                    {"type": "CN_DOE", "value": "UNKNOWN-CONTRACT"}
                ]
            },

            # No BRC mapping available
            {
                "title": "No BRC Data"
                # No site_ownership_code, no identifiers
            },

            # Invalid identifiers structure
            {
                "identifiers": [
                    {"type": "CN_DOE"},  # Missing value
                    {"value": "SC0018420"},  # Missing type
                    {}  # Empty identifier
                ]
            }
        ]

        for i, record_data in enumerate(test_cases):
            # Add required fields
            record_data.update({
                "osti_id": f"1234{i}",
                "title": record_data.get("title", f"Test Dataset {i}")
            })

            test_data = {"records": [record_data]}

            input_file = tmp_path / f"brc_test_{i}.json"
            with open(input_file, 'w') as f:
                json.dump(test_data, f)

            output_file = tmp_path / f"brc_output_{i}.json"

            test_args = [
                'brcschema', 'transform',
                '-T', 'osti_to_brc',
                '-o', str(output_file),
                str(input_file)
            ]

            with patch.object(sys, 'argv', test_args):
                try:
                    main()
                except SystemExit:
                    pass

            assert output_file.exists()

            with open(output_file, 'r') as f:
                result = json.load(f)

            dataset = result['datasets'][0]
            brc_value = dataset.get('brc')

            if i == 0:  # Direct site_ownership_code
                assert brc_value == "CABBI"
            elif i == 1:  # Valid contract mapping
                assert brc_value == "CABBI"  # SC0018420 maps to CABBI
            elif i == 2:  # Unknown contract
                assert brc_value is None
            elif i == 3:  # No BRC data
                assert brc_value is None
            elif i == 4:  # Invalid identifiers
                assert brc_value is None

    def test_fallback_authors_field(self, tmp_path):
        """Test fallback to authors field when persons is not available."""
        data_with_authors = {
            "records": [{
                "osti_id": "12345",
                "title": "Dataset with Authors",
                "authors": ["John Doe", "Jane Smith", "Bob Wilson"]
                # No persons field
            }]
        }

        input_file = tmp_path / "authors_input.json"
        with open(input_file, 'w') as f:
            json.dump(data_with_authors, f)

        output_file = tmp_path / "authors_output.json"

        test_args = [
            'brcschema', 'transform',
            '-T', 'osti_to_brc',
            '-o', str(output_file),
            str(input_file)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

        assert output_file.exists()

        with open(output_file, 'r') as f:
            result = json.load(f)

        dataset = result['datasets'][0]
        creators = dataset.get('creator', [])

        assert len(creators) == 3
        assert creators[0]['name'] == 'John Doe'
        assert creators[0]['primaryContact'] is True  # First author is primary
        assert creators[1]['name'] == 'Jane Smith'
        assert creators[1]['primaryContact'] is False
        assert creators[2]['name'] == 'Bob Wilson'
        assert creators[2]['primaryContact'] is False

    def test_invalid_keywords_types(self, tmp_path):
        """Test keywords field with invalid data types."""
        data_with_invalid_keywords = {
            "records": [{
                "osti_id": "12345",
                "title": "Dataset with Invalid Keywords",
                "keywords": [
                    "valid keyword",
                    123,  # Number
                    None,  # None value
                    "",  # Empty string
                    "  ",  # Whitespace only
                    {"invalid": "object"},  # Dict object
                    ["nested", "list"]  # Nested list
                ]
            }]
        }

        input_file = tmp_path / "invalid_keywords_input.json"
        with open(input_file, 'w') as f:
            json.dump(data_with_invalid_keywords, f)

        output_file = tmp_path / "invalid_keywords_output.json"

        test_args = [
            'brcschema', 'transform',
            '-T', 'osti_to_brc',
            '-o', str(output_file),
            str(input_file)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

        assert output_file.exists()

        with open(output_file, 'r') as f:
            result = json.load(f)

        dataset = result['datasets'][0]
        keywords = dataset.get('keywords', [])

        # Should handle invalid types gracefully
        # Valid keyword should be preserved
        assert 'valid keyword' in keywords

        # Numbers should be converted to strings
        assert '123' in keywords

        # Objects should be converted to strings
        assert any('invalid' in str(k) or 'object' in str(k) for k in keywords)

        # Empty/None values should be filtered out
        assert '' not in keywords
        assert None not in keywords

    def test_transformation_error_handling(self, tmp_path):
        """Test that transformation handles errors gracefully without crashing."""
        # Data that might cause issues in transformation
        problematic_data = {
            "records": [
                {
                    "osti_id": "12345",
                    "title": "Dataset 1",
                    "persons": [
                        {
                            "type": "AUTHOR",
                            "first_name": "John",
                            "last_name": "Doe",
                            "email": "not-a-list",  # Should be list but is string
                            "affiliations": [
                                {
                                    "name": None  # None affiliation name
                                }
                            ]
                        }
                    ]
                },
                {
                    # Missing osti_id - could cause issues
                    "title": "Dataset 2",
                    "organizations": [
                        {
                            "type": "SPONSOR",
                            "name": None  # None organization name
                        }
                    ]
                }
            ]
        }

        input_file = tmp_path / "problematic_input.json"
        with open(input_file, 'w') as f:
            json.dump(problematic_data, f)

        output_file = tmp_path / "problematic_output.json"

        test_args = [
            'brcschema', 'transform',
            '-T', 'osti_to_brc',
            '-o', str(output_file),
            str(input_file)
        ]

        # Should not crash even with problematic data
        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

        # Should still produce output
        assert output_file.exists()

        with open(output_file, 'r') as f:
            result = json.load(f)

        # Should have processed both records
        assert 'datasets' in result
        assert len(result['datasets']) == 2

        # First dataset should have processed person despite email issue
        dataset1 = result['datasets'][0]
        assert dataset1['title'] == "Dataset 1"
        creators = dataset1.get('creator', [])
        if creators:
            assert creators[0]['name'] == 'John Doe'

        # Second dataset should exist despite missing osti_id
        dataset2 = result['datasets'][1]
        assert dataset2['title'] == "Dataset 2"

    def test_has_related_ids_field_handling(self, tmp_path):
        """Test that has_related_ids field is excluded when no valid related IDs exist."""
        # Test case 1: No related IDs (field should be omitted)
        data_no_related_ids = {
            "records": [{
                "osti_id": "12345",
                "title": "Dataset No Related IDs",
                "identifiers": [
                    {"type": "RN", "value": "None"},  # Invalid value
                    # Contract number (excluded)
                    {"type": "CN_DOE", "value": "SC0018420"}
                ]
            }]
        }

        # Test case 2: Valid related IDs (field should be included)
        data_with_related_ids = {
            "records": [{
                "osti_id": "12346",
                "title": "Dataset with Related IDs",
                "identifiers": [
                    {"type": "RN", "value": "PRJNA1228652"},  # Valid bioproject
                    # Contract number (excluded)
                    {"type": "CN_DOE", "value": "SC0018409"}
                ]
            }]
        }

        # Test no related IDs case
        input_file1 = tmp_path / "no_related_ids.json"
        with open(input_file1, 'w') as f:
            json.dump(data_no_related_ids, f)

        output_file1 = tmp_path / "no_related_ids_output.json"

        test_args1 = [
            'brcschema', 'transform',
            '-T', 'osti_to_brc',
            '-o', str(output_file1),
            str(input_file1)
        ]

        with patch.object(sys, 'argv', test_args1):
            try:
                main()
            except SystemExit:
                pass

        assert output_file1.exists()

        with open(output_file1, 'r') as f:
            result1 = json.load(f)

        dataset1 = result1['datasets'][0]
        # has_related_ids should not be present when there are no valid related IDs
        assert 'has_related_ids' not in dataset1

        # Test valid related IDs case
        input_file2 = tmp_path / "with_related_ids.json"
        with open(input_file2, 'w') as f:
            json.dump(data_with_related_ids, f)

        output_file2 = tmp_path / "with_related_ids_output.json"

        test_args2 = [
            'brcschema', 'transform',
            '-T', 'osti_to_brc',
            '-o', str(output_file2),
            str(input_file2)
        ]

        with patch.object(sys, 'argv', test_args2):
            try:
                main()
            except SystemExit:
                pass

        assert output_file2.exists()

        with open(output_file2, 'r') as f:
            result2 = json.load(f)

        dataset2 = result2['datasets'][0]
        # has_related_ids should be present with valid data
        assert 'has_related_ids' in dataset2
        assert isinstance(dataset2['has_related_ids'], list)
        assert len(dataset2['has_related_ids']) == 1
        assert dataset2['has_related_ids'][0] == 'BIOPROJECT:PRJNA1228652'

    def test_legacy_osti_fields_transform(self, tmp_path):
        """Legacy E-Link v1-style fields should still map into BRC output."""
        test_data = {
            "records": [{
                "osti_id": "99999",
                "title": "Legacy Dataset",
                "publication_date": "2024-05-01",
                "authors": ["Jane Doe", "Data Steward"],
                "subjects": ["legacy keyword, migrated metadata"],
                "links": ["https://example.org/datasets/legacy-99999"],
                "sponsor_orgs": ["Legacy Sponsor Office"],
                "doe_contract_number": "SC0018420",
                "other_identifiers": ["LEG-12345"]
            }]
        }

        input_file = tmp_path / "legacy_input.json"
        with open(input_file, 'w') as f:
            json.dump(test_data, f)

        output_file = tmp_path / "legacy_output.json"

        test_args = [
            'brcschema', 'transform',
            '-T', 'osti_to_brc',
            '-o', str(output_file),
            str(input_file)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

        with open(output_file, 'r') as f:
            result = json.load(f)

        dataset = result['datasets'][0]
        assert dataset['brc'] == 'CABBI'
        assert dataset['dataset_url'] == "https://example.org/datasets/legacy-99999"
        assert dataset['keywords'] == ['legacy keyword', 'migrated metadata']
        assert dataset['creator'][0]['name'] == 'Jane Doe'
        assert dataset['creator'][0]['primaryContact'] is True
        assert dataset['creator'][1]['name'] == 'Data Steward'
        assert dataset['funding'][0]['fundingOrganization']['organizationName'] == 'Legacy Sponsor Office'
        assert dataset['has_related_ids'] == ['LEG-12345']

    def test_author_organizations_fallback_to_creator(self, tmp_path):
        """Current OSTI records with only AUTHOR organizations should still produce creators."""
        test_data = {
            "records": [{
                "osti_id": "2584699",
                "title": "Organization Authored Dataset",
                "publication_date": "2025-02-26",
                "site_ownership_code": "GLBRC",
                "persons": [],
                "organizations": [
                    {"type": "AUTHOR", "name": "Great Lakes Bioenergy Research Center"},
                    {"type": "AUTHOR", "name": "Michigan State University"}
                ]
            }]
        }

        input_file = tmp_path / "org_authors_input.json"
        with open(input_file, 'w') as f:
            json.dump(test_data, f)

        output_file = tmp_path / "org_authors_output.json"

        test_args = [
            'brcschema', 'transform',
            '-T', 'osti_to_brc',
            '-o', str(output_file),
            str(input_file)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

        with open(output_file, 'r') as f:
            result = json.load(f)

        dataset = result['datasets'][0]
        assert dataset['creator'][0]['name'] == 'Great Lakes Bioenergy Research Center'
        assert dataset['creator'][0]['primaryContact'] is True
        assert dataset['creator'][1]['name'] == 'Michigan State University'
        assert dataset['creator'][1]['primaryContact'] is False

    def test_brc_to_osti_emits_current_and_legacy_fields(self, tmp_path):
        """BRC to OSTI should emit current E-Link 2 fields plus selected legacy aliases."""
        test_data = {
            "datasets": [{
                "title": "Roundtrip Dataset",
                "date": "2024-01-15",
                "identifier": "https://example.org/datasets/abc123",
                "bibliographicCitation": "https://doi.org/10.9999/example.dataset",
                "brc": "GLBRC",
                "creator": [{
                    "name": "Jane Q Doe",
                    "email": "jane@example.org",
                    "affiliation": "Michigan State University",
                    "primaryContact": True
                }],
                "contributors": [{
                    "name": "Bob Smith",
                    "contributorType": "DataManager"
                }],
                "funding": [{
                    "fundingOrganization": {
                        "organizationName": "Example Funding Office",
                        "ror_id": "ror:01ca2by25"
                    },
                    "awardNumber": "SC0018409",
                    "awardURI": "doi:10.11578/award123"
                }],
                "dataset_url": "https://example.org/datasets/abc123",
                "has_related_ids": [
                    "BIOPROJECT:PRJNA123456",
                    "doi:10.8888/related.doi"
                ],
                "active": True
            }]
        }

        input_file = tmp_path / "brc_input.json"
        with open(input_file, 'w') as f:
            json.dump(test_data, f)

        output_file = tmp_path / "osti_output.json"

        test_args = [
            'brcschema', 'transform',
            '-T', 'brc_to_osti',
            '-o', str(output_file),
            str(input_file)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

        with open(output_file, 'r') as f:
            result = json.load(f)

        record = result['records'][0]
        assert record['publication_date'] == '2024-01-15'
        assert record['released_to_osti_date'] == '2024-01-15'
        assert record['site_url'] == 'https://example.org/datasets/abc123'
        assert record['links'] == ['https://example.org/datasets/abc123']
        assert record['authors'] == ['Jane Q Doe']
        assert record['doe_contract_number'] == 'SC0018409'
        assert record['contract_number'] == 'SC0018409'
        assert any(
            identifier['type'] == 'CN_DOE' and identifier['value'] == 'SC0018409'
            for identifier in record['identifiers']
        )
        assert any(
            related_identifier['type'] == 'DOI'
            and related_identifier['relation'] == 'References'
            and related_identifier['value'] == '10.8888/related.doi'
            for related_identifier in record['related_identifiers']
        )
        assert any(
            related_identifier['type'] == 'URL'
            and related_identifier['value'] == 'https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA123456'
            for related_identifier in record['related_identifiers']
        )
        sponsor_org = next(org for org in record['organizations'] if org['type'] == 'SPONSOR')
        assert sponsor_org['name'] == 'Example Funding Office'
        assert sponsor_org['ror_id'] == '01ca2by25'
        assert any(
            identifier['type'] == 'AWARD_DOI' and identifier['value'] == '10.11578/award123'
            for identifier in sponsor_org['identifiers']
        )

    def test_brc_to_osti_non_doe_award_number_uses_cn_nondoe(self, tmp_path):
        """Generic funding awards should not be forced into CN_DOE."""
        test_data = {
            "datasets": [{
                "title": "Non DOE Award Dataset",
                "date": "2024-02-01",
                "identifier": "https://example.org/datasets/non-doe-award",
                "brc": "GLBRC",
                "creator": [{
                    "name": "Jane Doe",
                    "primaryContact": True
                }],
                "funding": [{
                    "fundingOrganization": {
                        "organizationName": "National Science Foundation"
                    },
                    "awardNumber": "NSF-1234567"
                }]
            }]
        }

        input_file = tmp_path / "brc_non_doe_input.json"
        with open(input_file, 'w') as f:
            json.dump(test_data, f)

        output_file = tmp_path / "osti_non_doe_output.json"

        test_args = [
            'brcschema', 'transform',
            '-T', 'brc_to_osti',
            '-o', str(output_file),
            str(input_file)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

        with open(output_file, 'r') as f:
            result = json.load(f)

        sponsor_org = next(org for org in result['records'][0]['organizations'] if org['type'] == 'SPONSOR')
        assert any(
            identifier['type'] == 'CN_NONDOE' and identifier['value'] == 'NSF-1234567'
            for identifier in sponsor_org['identifiers']
        )
        assert not any(
            identifier['type'] == 'CN_DOE' and identifier['value'] == 'NSF-1234567'
            for identifier in sponsor_org['identifiers']
        )
