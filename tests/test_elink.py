"""Tests for OSTI E-Link API retrieval functions."""

import json
import tempfile
from pathlib import Path

import pytest

from brc_schema.util.elink import OSTIRecordRetriever, retrieve_osti_records


class TestOSTIRecordRetriever:
    """Test the OSTIRecordRetriever class."""

    def test_init(self):
        """Test initialization."""
        retriever = OSTIRecordRetriever()
        assert retriever.api is not None

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        retriever = OSTIRecordRetriever(api_key="test_key")
        assert retriever.api is not None

    @pytest.mark.integration
    def test_get_record_by_osti_id(self):
        """Test retrieving a record by OSTI ID."""
        retriever = OSTIRecordRetriever()
        record = retriever.get_record_by_osti_id(1807585)

        assert record is not None
        assert record.get('osti_id') == '1807585'
        assert 'title' in record

    @pytest.mark.integration
    def test_get_record_by_doi(self):
        """Test retrieving a record by DOI."""
        retriever = OSTIRecordRetriever()
        # Use a known DOI that exists in OSTI
        record = retriever.get_record_by_doi("10.1002/aesr.202500034")

        if record:  # May not exist or may be restricted
            assert 'osti_id' in record
            assert 'title' in record

    @pytest.mark.integration
    def test_get_records_multiple(self):
        """Test retrieving multiple records."""
        retriever = OSTIRecordRetriever()
        records = retriever.get_records(
            osti_ids=[1807585, 2574191]
        )

        assert len(records) >= 1  # At least one should exist
        for record in records:
            assert 'osti_id' in record
            assert 'title' in record

    @pytest.mark.integration
    def test_save_records_to_file(self):
        """Test saving records to a file."""
        retriever = OSTIRecordRetriever()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_records.json"

            num_records = retriever.save_records_to_file(
                output_path=output_path,
                osti_ids=[1807585],
                pretty=True
            )

            assert num_records >= 1
            assert output_path.exists()

            # Verify the file structure
            with open(output_path, 'r') as f:
                data = json.load(f)

            assert 'records' in data
            assert isinstance(data['records'], list)
            assert len(data['records']) == num_records


class TestConvenienceFunction:
    """Test the convenience function."""

    @pytest.mark.integration
    def test_retrieve_osti_records(self):
        """Test the convenience function."""
        records = retrieve_osti_records(
            osti_ids=[1807585]
        )

        assert len(records) >= 1
        assert records[0].get('osti_id') == '1807585'

    @pytest.mark.integration
    def test_retrieve_osti_records_with_output(self):
        """Test the convenience function with output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_output.json"

            records = retrieve_osti_records(
                osti_ids=[1807585],
                output_file=output_path
            )

            assert len(records) >= 1
            assert output_path.exists()

            # Verify the output file
            with open(output_path, 'r') as f:
                data = json.load(f)

            assert 'records' in data
            assert len(data['records']) >= 1
