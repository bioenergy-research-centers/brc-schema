"""Tests for OSTI E-Link API retrieval functions."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from brc_schema.util.elink import OSTIRecordRetriever, retrieve_osti_records


# Skip integration tests if no API key is available
OSTI_API_KEY = os.environ.get('OSTI_API_KEY')
skip_if_no_api_key = pytest.mark.skipif(
    not OSTI_API_KEY,
    reason="OSTI_API_KEY environment variable not set"
)


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
    @skip_if_no_api_key
    def test_get_record_by_osti_id(self):
        """Test retrieving a record by OSTI ID."""
        retriever = OSTIRecordRetriever()
        record = retriever.get_record_by_osti_id(2584700)

        assert record is not None
        assert record.get('osti_id') == '2584700'
        assert 'title' in record

    @pytest.mark.integration
    @skip_if_no_api_key
    def test_get_record_by_doi(self):
        """Test retrieving a record by OSTI-format DOI."""
        retriever = OSTIRecordRetriever()
        # Use a known OSTI-format DOI (10.11578/XXXXXXX)
        record = retriever.get_record_by_doi("10.11578/2584700")

        assert record is not None
        assert record.get('osti_id') == '2584700'
        assert 'title' in record
        assert record.get('doi') == '10.11578/2584700'

    @pytest.mark.integration
    @skip_if_no_api_key
    def test_get_record_by_doi_non_osti_format(self):
        """Test that non-OSTI DOI format returns None."""
        retriever = OSTIRecordRetriever()
        # Non-OSTI DOI should return None
        record = retriever.get_record_by_doi("10.1002/aesr.202500034")

        assert record is None

    @pytest.mark.integration
    @skip_if_no_api_key
    def test_get_records_multiple(self):
        """Test retrieving multiple records."""
        retriever = OSTIRecordRetriever()
        records = retriever.get_records(
            osti_ids=[2584700]
        )

        assert len(records) == 1
        for record in records:
            assert 'osti_id' in record
            assert 'title' in record

    @pytest.mark.integration
    @skip_if_no_api_key
    def test_save_records_to_file(self):
        """Test saving records to a file."""
        retriever = OSTIRecordRetriever()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_records.json"

            num_records = retriever.save_records_to_file(
                output_path=output_path,
                osti_ids=[2584700],
                pretty=True
            )

            assert num_records == 1
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
    @skip_if_no_api_key
    def test_retrieve_osti_records(self):
        """Test the convenience function."""
        records = retrieve_osti_records(
            osti_ids=[2584700]
        )

        assert len(records) == 1
        assert records[0].get('osti_id') == '2584700'

    @pytest.mark.integration
    @skip_if_no_api_key
    def test_retrieve_osti_records_with_output(self):
        """Test the convenience function with output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_output.json"

            records = retrieve_osti_records(
                osti_ids=[2584700],
                output_file=output_path
            )

            assert len(records) == 1
            assert output_path.exists()

            # Verify the output file
            with open(output_path, 'r') as f:
                data = json.load(f)

            assert 'records' in data
            assert len(data['records']) == 1
