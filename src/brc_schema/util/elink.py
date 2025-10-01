"""Wrappers for calling the E-Link API through its own module."""

import json
import logging
import os
from pathlib import Path
from typing import List, Union, Optional, Dict, Any

from elinkapi import Elink

logger = logging.getLogger(__name__)


class OSTIRecordRetriever:
    """Retrieve records from OSTI E-Link 2.0 API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OSTI record retriever.

        Args:
            api_key: Optional API key for authentication. If not provided,
                    will attempt to use OSTI_API_KEY environment variable.
        """
        # Use provided API key, or try to get from environment
        token = api_key or os.environ.get('OSTI_API_KEY')
        self.api = Elink(token=token)

        if token:
            logger.debug("Initialized with authentication token")
        else:
            logger.warning(
                "No API key provided - some records may not be accessible")

    def get_record_by_osti_id(self, osti_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single record by OSTI ID.

        Args:
            osti_id: The OSTI ID to retrieve (e.g., 2562995)

        Returns:
            Dictionary containing the record metadata, or None if not found
        """
        try:
            logger.info(f"Retrieving record for OSTI ID: {osti_id}")
            record = self.api.get_single_record(osti_id=str(osti_id))

            if record:
                # Convert Record object to dictionary
                return self.api.record_to_dict(record)
            else:
                logger.warning(f"No record found for OSTI ID: {osti_id}")
                return None

        except Exception as e:
            logger.error(f"Error retrieving OSTI ID {osti_id}: {e}")
            return None

    def get_record_by_doi(self, doi: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single record by DOI.

        Args:
            doi: The DOI to retrieve (e.g., "10.1002/aesr.202500034")

        Returns:
            Dictionary containing the record metadata, or None if not found
        """
        try:
            # Clean DOI if it includes the full URL
            if doi.startswith('http'):
                doi = doi.split('doi.org/')[-1]

            logger.info(f"Retrieving record for DOI: {doi}")
            record = self.api.get_single_record(doi=doi)

            if record:
                # Convert Record object to dictionary
                return self.api.record_to_dict(record)
            else:
                logger.warning(f"No record found for DOI: {doi}")
                return None

        except Exception as e:
            logger.error(f"Error retrieving DOI {doi}: {e}")
            return None

    def get_records(
        self,
        osti_ids: Optional[List[Union[int, str]]] = None,
        dois: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve multiple records by OSTI IDs and/or DOIs.

        Args:
            osti_ids: List of OSTI IDs to retrieve
            dois: List of DOIs to retrieve

        Returns:
            List of record dictionaries
        """
        records = []

        # Retrieve records by OSTI ID
        if osti_ids:
            for osti_id in osti_ids:
                record = self.get_record_by_osti_id(osti_id)
                if record:
                    records.append(record)

        # Retrieve records by DOI
        if dois:
            for doi in dois:
                record = self.get_record_by_doi(doi)
                if record:
                    records.append(record)

        logger.info(f"Retrieved {len(records)} records total")
        return records

    def save_records_to_file(
        self,
        output_path: Union[str, Path],
        osti_ids: Optional[List[Union[int, str]]] = None,
        dois: Optional[List[str]] = None,
        pretty: bool = True
    ) -> int:
        """
        Retrieve records and save them to a JSON file.

        Args:
            output_path: Path to output JSON file
            osti_ids: List of OSTI IDs to retrieve
            dois: List of DOIs to retrieve
            pretty: Whether to pretty-print the JSON (default: True)

        Returns:
            Number of records written to file
        """
        records = self.get_records(osti_ids=osti_ids, dois=dois)

        if not records:
            logger.warning("No records retrieved to save")
            return 0

        # Create output structure matching OSTI schema
        output_data = {
            "records": records
        }

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(output_data, f, ensure_ascii=False)

        logger.info(f"Saved {len(records)} records to {output_path}")
        return len(records)


def retrieve_osti_records(
    osti_ids: Optional[List[Union[int, str]]] = None,
    dois: Optional[List[str]] = None,
    output_file: Optional[Union[str, Path]] = None,
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Convenience function to retrieve OSTI records.

    Args:
        osti_ids: List of OSTI IDs to retrieve
        dois: List of DOIs to retrieve
        output_file: Optional path to save records as JSON
        api_key: Optional API key for authentication

    Returns:
        List of record dictionaries

    Example:
        >>> records = retrieve_osti_records(
        ...     osti_ids=[2562995, 2574191],
        ...     dois=["10.1002/aesr.202500034"],
        ...     output_file="osti_records.json"
        ... )
    """
    retriever = OSTIRecordRetriever(api_key=api_key)

    if output_file:
        retriever.save_records_to_file(
            output_path=output_file,
            osti_ids=osti_ids,
            dois=dois
        )

    return retriever.get_records(osti_ids=osti_ids, dois=dois)
