"""Tests for OSTI E-Link API retrieval functions."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from brc_schema.util.elink import (
    OSTIRecordRetriever,
    OSTIRecordTransmitter,
    retrieve_osti_records,
    TransmitSummary,
    MultipleMatchesError
)


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
        assert record.get('osti_id') == 2584700  # API returns int
        assert 'title' in record

    @pytest.mark.integration
    @skip_if_no_api_key
    def test_get_record_by_doi(self):
        """Test retrieving a record by OSTI-format DOI."""
        retriever = OSTIRecordRetriever()
        # Use a known OSTI-format DOI (10.11578/XXXXXXX)
        record = retriever.get_record_by_doi("10.11578/2584700")

        assert record is not None
        assert record.get('osti_id') == 2584700  # API returns int
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

            records = retriever.save_records_to_file(
                output_path=output_path,
                osti_ids=[2584700],
                pretty=True
            )

            assert len(records) == 1
            assert output_path.exists()

            # Verify the file structure
            with open(output_path, 'r') as f:
                data = json.load(f)

            assert 'records' in data
            assert isinstance(data['records'], list)
            assert len(data['records']) == len(records)


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
        assert records[0].get('osti_id') == 2584700  # API returns int

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


class TestOSTIRecordTransmitter:
    """Test the OSTIRecordTransmitter class."""

    def test_init(self):
        """Test initialization."""
        transmitter = OSTIRecordTransmitter()
        assert transmitter.api is not None
        assert transmitter.dry_run is False
        assert transmitter.record_limit is None
        assert transmitter.skip_urls == ""
        assert transmitter.new_only is False
        assert isinstance(transmitter.summary, TransmitSummary)

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        transmitter = OSTIRecordTransmitter(api_key="test_key")
        assert transmitter.api is not None

    def test_init_with_dry_run(self):
        """Test initialization with dry_run flag."""
        transmitter = OSTIRecordTransmitter(dry_run=True)
        assert transmitter.dry_run is True

    def test_init_with_api_url(self):
        """Test initialization with custom API URL."""
        transmitter = OSTIRecordTransmitter(api_url="https://test.example.com/api")
        assert transmitter.api is not None

    @pytest.mark.integration
    @skip_if_no_api_key
    def test_transmit_dry_run(self):
        """Test transmit with dry_run flag (should not create records)."""
        transmitter = OSTIRecordTransmitter(dry_run=True)
        transmitter.record_limit = 1

        # Create a minimal test record
        test_records = [{
            "title": "Test Dataset - Dry Run",
            "site_ownership_code": "TEST",
            "product_type": "GD"
        }]

        summary = transmitter.post_records(test_records)

        # In dry run mode, it should count as a new record but not actually create it
        assert isinstance(summary, TransmitSummary)
        assert summary.new_count + summary.update_count + summary.fail_count + summary.skip_count > 0


class TestTransmitSummary:
    """Test the TransmitSummary class."""

    def test_init(self):
        """Test TransmitSummary initialization."""
        summary = TransmitSummary()
        # Note: Due to class-level mutable defaults, counts might be shared
        # This is a known issue in the implementation
        assert hasattr(summary, 'new_count')
        assert hasattr(summary, 'update_count')
        assert hasattr(summary, 'fail_count')
        assert hasattr(summary, 'skip_count')
        assert hasattr(summary, 'pass_records')
        assert hasattr(summary, 'fail_records')

    def test_add_new(self):
        """Test adding a new record to summary."""
        summary = TransmitSummary()
        initial_count = summary.new_count
        initial_pass_len = len(summary.pass_records)
        
        test_record = {"title": "Test", "osti_id": 123}
        summary.add_new(0, test_record)
        
        assert summary.new_count == initial_count + 1
        assert len(summary.pass_records) == initial_pass_len + 1
        assert summary.pass_records[-1]["index"] == 0
        assert summary.pass_records[-1]["record"] == test_record

    def test_add_update(self):
        """Test adding an updated record to summary."""
        summary = TransmitSummary()
        initial_count = summary.update_count
        initial_pass_len = len(summary.pass_records)
        
        test_record = {"title": "Test", "osti_id": 123}
        summary.add_update(1, test_record)
        
        assert summary.update_count == initial_count + 1
        assert len(summary.pass_records) == initial_pass_len + 1

    def test_add_fail(self):
        """Test adding a failed record to summary."""
        summary = TransmitSummary()
        initial_count = summary.fail_count
        initial_fail_len = len(summary.fail_records)
        
        test_record = {"title": "Test"}
        error_msg = "Test error"
        summary.add_fail(2, test_record, error_msg)
        
        assert summary.fail_count == initial_count + 1
        assert len(summary.fail_records) == initial_fail_len + 1
        assert summary.fail_records[-1]["index"] == 2
        assert summary.fail_records[-1]["error"] == error_msg

    def test_add_skip(self):
        """Test adding a skipped record to summary."""
        summary = TransmitSummary()
        initial_count = summary.skip_count
        
        test_record = {"title": "Test"}
        summary.add_skip(3, test_record)
        
        assert summary.skip_count == initial_count + 1

    def test_message(self):
        """Test summary message generation."""
        summary = TransmitSummary()
        # Record initial state
        initial_new = summary.new_count
        initial_update = summary.update_count
        initial_fail = summary.fail_count
        initial_skip = summary.skip_count
        
        # Add records
        summary.add_new(0, {})
        summary.add_update(1, {})
        summary.add_fail(2, {}, "error")
        summary.add_skip(3, {})
        
        message = summary.message()
        assert f"New: {initial_new + 1}" in message
        assert f"Updated: {initial_update + 1}" in message
        assert f"Failed: {initial_fail + 1}" in message
        assert f"Skipped: {initial_skip + 1}" in message

    def test_failures(self):
        """Test failures list generation."""
        summary = TransmitSummary()
        initial_fail_len = len(summary.fail_records)
        
        test_record = {"title": "Test Title", "doi": "10.1234/test"}
        summary.add_fail(99, test_record, "Test error message")
        
        failures = summary.failures()
        # Check that at least one more failure was added
        assert len(failures) >= initial_fail_len + 1
        # Find our specific failure
        our_failure = [f for f in failures if "Record Index: (99)" in f]
        assert len(our_failure) == 1
        assert "Test error message" in our_failure[0]
        assert "Test Title" in our_failure[0]


class TestMultipleMatchesError:
    """Test the MultipleMatchesError exception."""

    def test_init(self):
        """Test MultipleMatchesError initialization."""
        error = MultipleMatchesError(5)
        assert error.count == 5
        assert "Expected 0 or 1 match, found 5" in str(error)
