"""Wrappers for calling the E-Link API through its own module."""

import json
import logging
import os
import base64
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path
from typing import List, Union, Optional, Dict, Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from elinkapi import Elink, Record, exceptions

logger = logging.getLogger(__name__)

OSTI_DOI_PREFIX = "10.11578/"
OSTI_PUBLIC_API_RECORDS_URL = "https://www.osti.gov/api/v1/records"
OSTI_LEGACY_ELINK_API_URL = "https://www.osti.gov/elink/2416api"
OSTI_ELINK_ORIGIN_SCHEMA = "osti_elink2_json"
OSTI_LEGACY_ORIGIN_SCHEMA = "osti_elink1_xml"
OSTI_PUBLIC_ORIGIN_SCHEMA = "osti_public_api_v1_json"
OSTI_NORMALIZED_SCHEMA = "osti_schema"
OSTI_SOURCE_METADATA = {
    "elink2": {
        "api": "elink2",
        "origin_schema": OSTI_ELINK_ORIGIN_SCHEMA,
        "normalized_schema": OSTI_NORMALIZED_SCHEMA,
    },
    "legacy": {
        "api": "legacy",
        "origin_schema": OSTI_LEGACY_ORIGIN_SCHEMA,
        "normalized_schema": OSTI_NORMALIZED_SCHEMA,
    },
    "public": {
        "api": "public",
        "origin_schema": OSTI_PUBLIC_ORIGIN_SCHEMA,
        "normalized_schema": OSTI_NORMALIZED_SCHEMA,
    },
}


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles date and datetime objects."""

    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


class OSTIRecordRetriever:
    """Retrieve records from OSTI E-Link and public OSTI.GOV APIs."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        legacy_api_url: str = OSTI_LEGACY_ELINK_API_URL,
        legacy_username: Optional[str] = None,
        legacy_password: Optional[str] = None,
        public_api_url: str = OSTI_PUBLIC_API_RECORDS_URL,
        initialize_elink2: bool = True,
    ):
        """
        Initialize the OSTI record retriever.

        Args:
            api_key: Optional E-Link 2.0 API key. If not provided, this will
                attempt to use OSTI_API_KEY from the environment.
            legacy_username: Optional legacy E-Link 1 username. If not
                provided, this will attempt to use OSTI_LEGACY_USERNAME.
            legacy_password: Optional legacy E-Link 1 password. If not
                provided, this will attempt to use OSTI_LEGACY_PASSWORD.
            initialize_elink2: Initialize the E-Link 2.0 client. Site-code
                retrieval can disable this when E-Link 2.0 is not selected.
        """
        # Use provided API key, or try to get from environment
        self.api = _init_api(api_key, api_url) if initialize_elink2 else None
        self.legacy_api_url = legacy_api_url
        self.legacy_username = legacy_username or os.environ.get("OSTI_LEGACY_USERNAME")
        self.legacy_password = legacy_password or os.environ.get("OSTI_LEGACY_PASSWORD")
        self.public_api_url = public_api_url

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

        Note: The E-Link API's get_single_record method only accepts OSTI IDs.
        For DOIs in the format "10.11578/XXXXXXX", we extract the OSTI ID
        from the last part. For other DOI formats, this method may not work.

        Args:
            doi: The DOI to retrieve (e.g., "10.11578/2584700")

        Returns:
            Dictionary containing the record metadata, or None if not found
        """
        try:
            # Clean DOI if it includes the full URL
            if doi.startswith('http'):
                doi = doi.split('doi.org/')[-1]

            logger.info(f"Retrieving record for DOI: {doi}")

            # Extract OSTI ID from DOI
            # OSTI DOIs typically follow the pattern: 10.11578/OSTI_ID
            if doi.startswith(OSTI_DOI_PREFIX):
                osti_id = doi.split('/')[-1]
                logger.debug(f"Extracted OSTI ID {osti_id} from DOI {doi}")

                # Use the OSTI ID retrieval method
                return self.get_record_by_osti_id(osti_id)
            else:
                logger.warning(
                    f"DOI {doi} does not follow the expected OSTI format (10.11578/XXXXXXX). "
                    "Cannot extract OSTI ID. Consider using OSTI ID directly."
                )
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

        In the case of duplicate records,
        only one instance of each record will be returned.

        Args:
            osti_ids: List of OSTI IDs to retrieve
            dois: List of DOIs to retrieve

        Returns:
            List of record dictionaries (duplicates removed)
        """
        records = []
        seen_osti_ids = set()

        # Retrieve records by OSTI ID
        if osti_ids:
            for osti_id in osti_ids:
                osti_id_str = str(osti_id)
                if osti_id_str not in seen_osti_ids:
                    # Mark as seen before retrieval
                    seen_osti_ids.add(osti_id_str)
                    record = self.get_record_by_osti_id(osti_id)
                    if record:
                        records.append(record)

        # Retrieve records by DOI
        if dois:
            for doi in dois:
                # Extract OSTI ID from DOI if possible to check for duplicates
                if doi.startswith('http'):
                    doi_clean = doi.split('doi.org/')[-1]
                else:
                    doi_clean = doi

                # Check if this is an OSTI DOI and extract the ID
                if doi_clean.startswith(OSTI_DOI_PREFIX):
                    osti_id_from_doi = doi_clean.split('/')[-1]
                    if osti_id_from_doi in seen_osti_ids:
                        logger.info(
                            f"Skipping DOI {doi} - already retrieved as OSTI ID {osti_id_from_doi}")
                        continue

                record = self.get_record_by_doi(doi)
                if record:
                    # Extract OSTI ID from the retrieved record to track it
                    if 'osti_id' in record:
                        seen_osti_ids.add(str(record['osti_id']))
                    records.append(record)

        logger.info(f"Retrieved {len(records)} records total")
        return records

    def query_elink2_records(
        self,
        site_code: str,
        product_type: Optional[str] = None,
        entry_date_start: Optional[str] = None,
        entry_date_end: Optional[str] = None,
        rows: int = 500,
        limit: Optional[int] = None,
    ) -> tuple[list[dict], dict]:
        """Query E-Link 2.0 records for a submitting site code."""
        params = {
            "site_ownership_code": site_code,
            "rows": rows,
        }
        if product_type:
            params["product_type"] = product_type
        if entry_date_start:
            params["entry_date_start"] = _format_osti_api_date(entry_date_start)
        if entry_date_end:
            params["entry_date_end"] = _format_osti_api_date(entry_date_end)

        query = self.api.query_records(**params)
        records = []
        for idx, record in enumerate(query):
            if limit is not None and idx >= limit:
                break
            records.append(self.api.record_to_dict(record))

        source_metadata = _source_metadata(
            source="elink2",
            query_params=params,
            total_rows=query.total_rows,
            record_count=len(records),
        )
        return records, source_metadata

    def query_legacy_records(
        self,
        site_code: str,
        product_type: Optional[str] = None,
        entry_date_start: Optional[str] = None,
        entry_date_end: Optional[str] = None,
        rows: int = 500,
        limit: Optional[int] = None,
    ) -> tuple[list[dict], dict]:
        """Query legacy E-Link 1 XML records for a submitting site code."""
        params = {
            "site_input_code": site_code,
            "rows": rows,
        }
        if product_type:
            params["product_type"] = product_type
        if entry_date_start:
            params["entry_date_start"] = _format_osti_api_date(entry_date_start)
        if entry_date_end:
            params["entry_date_end"] = _format_osti_api_date(entry_date_end)
        if limit is not None:
            params["rows"] = min(rows, limit)

        records, response_metadata = self._query_legacy_api(params)
        if limit is not None:
            records = records[:limit]

        source_metadata = _source_metadata(
            source="legacy",
            query_params=params,
            total_rows=response_metadata.get("total_rows"),
            record_count=len(records),
        )
        return records, source_metadata

    def query_public_records(
        self,
        site_code: str,
        product_type: Optional[str] = None,
        entry_date_start: Optional[str] = None,
        entry_date_end: Optional[str] = None,
        rows: int = 500,
        limit: Optional[int] = None,
    ) -> tuple[list[dict], dict]:
        """Query public OSTI.GOV records using legacy-shaped public record fields."""
        params = {
            "site_ownership_code": site_code,
            "rows": rows,
            "sort": "entry_date",
            "order": "desc",
        }
        if product_type:
            params["product_type"] = product_type
        if entry_date_start:
            params["entry_date_start"] = _format_osti_api_date(entry_date_start)
        if entry_date_end:
            params["entry_date_end"] = _format_osti_api_date(entry_date_end)
        if limit is not None:
            params["rows"] = min(rows, limit)

        records, response_metadata = self._query_public_api(params)
        if limit is not None:
            records = records[:limit]

        source_metadata = _source_metadata(
            source="public",
            query_params=params,
            total_rows=response_metadata.get("total_rows"),
            record_count=len(records),
        )
        return records, source_metadata

    def retrieve_records_by_site_code(
        self,
        site_code: str,
        sources: tuple[str, ...] = ("legacy", "elink2"),
        product_type: Optional[str] = None,
        entry_date_start: Optional[str] = None,
        entry_date_end: Optional[str] = None,
        rows: int = 500,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve records for a site code from one or more OSTI source APIs."""
        site_code = site_code.strip().upper()
        records = []
        record_origins = []
        retrieval_sources = []

        for source in sources:
            if source == "legacy":
                source_records, source_metadata = self.query_legacy_records(
                    site_code=site_code,
                    product_type=product_type,
                    entry_date_start=entry_date_start,
                    entry_date_end=entry_date_end,
                    rows=rows,
                    limit=limit,
                )
            elif source == "elink2":
                source_records, source_metadata = self.query_elink2_records(
                    site_code=site_code,
                    product_type=product_type,
                    entry_date_start=entry_date_start,
                    entry_date_end=entry_date_end,
                    rows=rows,
                    limit=limit,
                )
            elif source == "public":
                source_records, source_metadata = self.query_public_records(
                    site_code=site_code,
                    product_type=product_type,
                    entry_date_start=entry_date_start,
                    entry_date_end=entry_date_end,
                    rows=rows,
                    limit=limit,
                )
            else:
                raise ValueError(f"Unknown OSTI source API: {source}")

            retrieval_sources.append(source_metadata)
            origin_schema = source_metadata["origin_schema"]
            for record in source_records:
                record_origins.append(
                    {
                        "record_index": len(records),
                        "osti_id": record.get("osti_id"),
                        "source": source,
                        "origin_schema": origin_schema,
                        "normalized_schema": OSTI_NORMALIZED_SCHEMA,
                    }
                )
                records.append(record)

        return {
            "source_query": {
                "site_code": site_code,
                "product_type": product_type,
                "entry_date_start": entry_date_start,
                "entry_date_end": entry_date_end,
                "sources": list(sources),
            },
            "retrieval_sources": retrieval_sources,
            "record_origins": record_origins,
            "records": records,
        }

    def save_records_by_site_code_to_file(
        self,
        output_path: Union[str, Path],
        site_code: str,
        sources: tuple[str, ...] = ("legacy", "elink2"),
        product_type: Optional[str] = None,
        entry_date_start: Optional[str] = None,
        entry_date_end: Optional[str] = None,
        rows: int = 500,
        limit: Optional[int] = None,
        pretty: bool = True,
    ) -> dict:
        """Retrieve site-code records and save them with source-origin metadata."""
        output_data = self.retrieve_records_by_site_code(
            site_code=site_code,
            sources=sources,
            product_type=product_type,
            entry_date_start=entry_date_start,
            entry_date_end=entry_date_end,
            rows=rows,
            limit=limit,
        )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(output_data, f, indent=2,
                          ensure_ascii=False, cls=DateTimeEncoder)
            else:
                json.dump(output_data, f, ensure_ascii=False,
                          cls=DateTimeEncoder)

        logger.info(
            f"Saved {len(output_data['records'])} site-code record(s) to {output_path}")
        return output_data

    def _query_legacy_api(self, params: dict) -> tuple[list[dict], dict]:
        if not self.legacy_username or not self.legacy_password:
            raise ValueError(
                "Legacy E-Link 1 retrieval requires basic-auth credentials. "
                "Provide --legacy-username/--legacy-password or set "
                "OSTI_LEGACY_USERNAME and OSTI_LEGACY_PASSWORD."
            )
        query_url = f"{self.legacy_api_url}?{urlencode(params)}"
        credentials = f"{self.legacy_username}:{self.legacy_password}".encode("utf-8")
        auth_header = base64.b64encode(credentials).decode("ascii")
        request = Request(
            query_url,
            headers={
                "Accept": "application/xml",
                "Authorization": f"Basic {auth_header}",
            },
        )
        with urlopen(request) as response:
            payload = response.read().decode("utf-8")
            total_rows = response.headers.get("X-Total-Count")
        records = _parse_legacy_elink_xml(payload)
        return records, {
            "total_rows": int(total_rows) if total_rows is not None else len(records),
        }

    def _query_public_api(self, params: dict) -> tuple[list[dict], dict]:
        query_url = f"{self.public_api_url}?{urlencode(params)}"
        request = Request(query_url, headers={"Accept": "application/json"})
        with urlopen(request) as response:
            payload = response.read().decode("utf-8")
            total_rows = response.headers.get("X-Total-Count")
        records = json.loads(payload)
        if isinstance(records, dict):
            records = [records]
        return records, {
            "total_rows": int(total_rows) if total_rows is not None else None,
        }

    def save_records_to_file(
        self,
        output_path: Union[str, Path],
        osti_ids: Optional[List[Union[int, str]]] = None,
        dois: Optional[List[str]] = None,
        pretty: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Retrieve records and save them to a JSON file.

        Args:
            output_path: Path to output JSON file
            osti_ids: List of OSTI IDs to retrieve
            dois: List of DOIs to retrieve
            pretty: Whether to pretty-print the JSON (default: True)

        Returns:
            List of records written to file
        """
        records = self.get_records(osti_ids=osti_ids, dois=dois)

        if not records:
            logger.warning("No records retrieved to save")
            records = []

        # Create output structure matching OSTI schema
        output_data = {
            "records": records
        }

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(output_data, f, indent=2,
                          ensure_ascii=False, cls=DateTimeEncoder)
            else:
                json.dump(output_data, f, ensure_ascii=False,
                          cls=DateTimeEncoder)

        logger.info(f"Saved {len(records)} records to {output_path}")
        return records


def retrieve_osti_records(
    osti_ids: Optional[List[Union[int, str]]] = None,
    dois: Optional[List[str]] = None,
    output_file: Optional[Union[str, Path]] = None,
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Convenience function to retrieve OSTI records.

    Note: DOIs must be in OSTI format (10.11578/XXXXXXX) where XXXXXXX is the OSTI ID.
    Non-OSTI DOIs will be skipped with a warning.

    Args:
        osti_ids: List of OSTI IDs to retrieve
        dois: List of DOIs to retrieve (must be in OSTI format: 10.11578/XXXXXXX)
        output_file: Optional path to save records as JSON
        api_key: Optional API key for authentication

    Returns:
        List of record dictionaries

    Example:
        >>> records = retrieve_osti_records(
        ...     osti_ids=[2584700, 2574191],
        ...     dois=["10.11578/2584700"],
        ...     output_file="osti_records.json"
        ... )
    """
    retriever = OSTIRecordRetriever(api_key=api_key)

    if output_file:
        # save_records_to_file returns the records it retrieved
        return retriever.save_records_to_file(
            output_path=output_file,
            osti_ids=osti_ids,
            dois=dois
        )

    return retriever.get_records(osti_ids=osti_ids, dois=dois)


def _format_osti_api_date(value):
    """Format ISO dates as the MM/DD/YYYY query dates accepted by OSTI APIs."""
    if not value:
        return None
    value = str(value).strip()
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return value
    return parsed.strftime("%m/%d/%Y")


def _parse_legacy_elink_xml(payload: str) -> list[dict]:
    root = ET.fromstring(payload)
    if _strip_namespace(root.tag) == "record":
        record_elements = [root]
    else:
        record_elements = [
            element for element in root.iter()
            if _strip_namespace(element.tag) == "record"
        ]
    return [_xml_element_to_dict(element) for element in record_elements]


def _xml_element_to_dict(element):
    children = list(element)
    if not children:
        text = element.text.strip() if element.text else ""
        return text or None

    result = {}
    for child in children:
        key = _legacy_key(_strip_namespace(child.tag))
        value = _xml_element_to_dict(child)
        if key in result:
            if not isinstance(result[key], list):
                result[key] = [result[key]]
            result[key].append(value)
        else:
            result[key] = value
    return result


def _strip_namespace(tag):
    return tag.rsplit("}", 1)[-1]


def _legacy_key(key):
    return {
        "site_input_code": "site_ownership_code",
        "contract_nos": "doe_contract_number",
        "originating_research_org": "research_orgs",
        "sponsor_org": "sponsor_orgs",
    }.get(key, key)


def _source_metadata(source, query_params, total_rows, record_count):
    metadata = dict(OSTI_SOURCE_METADATA[source])
    metadata.update(
        {
            "query_params": {key: value for key, value in query_params.items() if value is not None},
            "total_rows": total_rows,
            "record_count": record_count,
        }
    )
    return metadata


class MultipleMatchesError(Exception):
    """Raised when more than one existing matching record is found while attempting to transmit record data."""

    def __init__(self, count):
        self.count = count
        super().__init__(f"Expected 0 or 1 match, found {count}")


class TransmitSummary:
    def __init__(self):
        self.new_count: int = 0
        self.update_count: int = 0
        self.fail_count: int = 0
        self.skip_count: int = 0
        self.pass_records: list = []
        self.fail_records: list = []

    def add_new(self, index, record):
        self.new_count += 1
        self.pass_records.append({"index": index, "record": record})

    def add_update(self, index, record):
        self.update_count += 1
        self.pass_records.append({"index": index, "record": record})

    def add_fail(self, index, record, error):
        self.fail_count += 1
        self.fail_records.append(
            {"index": index, "record": record, "error": error})

    def add_skip(self, index, record):
        self.skip_count += 1

    def message(self):
        return f"Transmit Summary - New: {self.new_count}, Updated: {self.update_count}, Skipped: {self.skip_count}, Failed: {self.fail_count}"

    def failures(self):
        failure_data = []
        for f in self.fail_records:
            idx = f.get("index", "?")
            error = f.get("error", "unknown")
            record = f.get("record", {})
            doi = record.get('doi', '?')
            identifiers = record.get('identifiers', '?')
            title = record.get('title', '?')
            failure_data.append(
                f"Transmit Failure - Record Index: ({idx}),  Error: {error}, Record: doi='{doi}'; identifiers='{identifiers}'; title='{title}'")
        return failure_data


class OSTIRecordTransmitter:
    """Transmit records into OSTI using E-Link 2.0 API."""

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None, dry_run: bool = False):
        """
        Initialize the OSTI record transmitter.

        Args:
            api_key: Optional API key for authentication. If not provided,
                    will attempt to use OSTI_API_KEY environment variable.
        """
        # Use provided API key, or try to get from environment
        self.api = _init_api(api_key, api_url)
        self.dry_run: bool = dry_run
        self.record_limit: Optional[int] = None
        self.skip_urls: str = ""
        self.new_only: bool = False
        self.summary: TransmitSummary = TransmitSummary()

    def _process_unique_record_query(self, query, search_attribute, record_data, raise_on_multiple=False):
        if query.total_rows == 1:
            return query.data[0].osti_id
        elif query.total_rows > 1:
            logger.info(
                f"Multiple existing matches found for record by {search_attribute}: '{record_data}'. Total Existing Matches: {query.total_rows}")
            # Output found records for inspection
            for idx, osti_record in enumerate(query):
                attr_value = repr(getattr(osti_record, search_attribute, "?"))
                logger.info(
                    f"\t -- Existing Match - OSTI ID: {osti_record.osti_id}, {search_attribute} : {attr_value}")
                if idx > 9:
                    logger.info(
                        f"\t -- ... Existing Match Output Truncated ...")
                    break
            if raise_on_multiple:
                raise MultipleMatchesError(query.total_rows)
        else:
            return None

    def find_existing_record_id(self, new_record: Record) -> Optional[int]:
        """
        Use provided attributes to perform a best-effort lookup for any existing records.
        Raises an error if multiple matches are found.

        Args:
          record_data: A Record with data to lookup.

        Returns:
          OSTI identifier for the single uniquely found record, or None.

        """
        # Search for existing records to avoid creating duplicates.
        new_osti_id = None
        # try matching unique doi
        if new_record.doi:
            query = self.api.query_records(
                product_type=new_record.product_type,
                site_ownership_code=new_record.site_ownership_code,
                doi=new_record.doi,
            )
            # raise errors if duplicate DOI found. Should not be possible unless record doi is invalid/incomplete
            new_osti_id = self._process_unique_record_query(
                query, 'doi', new_record.doi, True)
            if new_osti_id:
                return new_osti_id

        # try matching other identifiers
        if new_record.identifiers:
            for identifier in new_record.identifiers:
                if identifier.type != 'OTHER_ID':
                    continue
                query = self.api.query_records(
                    product_type=new_record.product_type,
                    site_ownership_code=new_record.site_ownership_code,
                    identifiers=identifier.value,
                )
                new_osti_id = self._process_unique_record_query(
                    query, 'identifiers', identifier.value, False)  # Try next lookup without error
                if new_osti_id:
                    return new_osti_id

        # try matching unique title
        query = self.api.query_records(
            product_type=new_record.product_type,
            site_ownership_code=new_record.site_ownership_code,
            title=new_record.title,
        )
        # Last check, raise errors if multiple items found
        return self._process_unique_record_query(query, 'title', new_record.title, True)

    def transmit_osti_record(
        self,
        record_data: Dict,
        index: int,
    ) -> Optional[Record]:
        """
        Function to create a single OSTI record.

        Uses the Elink Record Pydantic model to validate and then POST to the Elink API.


        Args:
            record_data: A dictionary of data for the new record.

        Returns:
            Record object saved to OSTI.

        Example:
            >>> record_json = {
            ...     "title": "A Dissertation Title",
            ...     "site_ownership_code": "AAAA",
            ...     "product_type": "TD" 
            ... }
            ... record = transmit_osti_record(
            ...     record_data = record_json
            ... )
        """

        logger.debug(f"Importing new OSTI dataset: {record_data}")

        # Build record and validate with Pydantic
        new_record = Record(**record_data)
        if not new_record.osti_id:
            # Check for existing records and assign osti_id if a unique item is found
            # This will raise an error if multiple matches are found
            # Assigning osti_id to 'None' causes API errors. Only assign if found
            found_osti_id = self.find_existing_record_id(new_record)
            if found_osti_id:
                new_record.osti_id = found_osti_id

        # POST record through API and return result
        saved_record = None
        # Records with osti_id get updated
        if new_record.osti_id:
            if self.dry_run:
                logger.warning(
                    f"Dry Run: skipping update for existing record (counted as an 'update' in summary) ({new_record.osti_id}):' {new_record.title}'")
                saved_record = new_record
            elif self.new_only:
                logger.warning(
                    f"New Only: skipping update for existing record (counted as 'update' in summary) ({new_record.osti_id}):' {new_record.title}'")
                saved_record = new_record
            else:
                logger.info(
                    f"Updating existing record ({new_record.osti_id}):' {new_record.title}'")
                saved_record = self.api.update_record(
                    new_record.osti_id, new_record, "submit")
            self.summary.add_update(index, record_data)
        # Records without osti_id get created
        else:
            if self.dry_run:
                logger.warning(
                    f"dry run, skipping save for new record: '{new_record.title}'")
                saved_record = new_record
            else:
                logger.info(f"Saving new record: '{new_record.title}'")
                saved_record = self.api.post_new_record(new_record, "submit")
            self.summary.add_new(index, record_data)

        return saved_record

    def post_records(
        self,
        records: List[Dict]
    ):
        """
        Transmit multiple records.

        Args:
          records: List of OSTI formatted record dictionaries

        Returns:
          A TransmitSummary instance
        """
        self.summary = TransmitSummary()
        # Handle missing or empty list
        if not records:
            return self.summary

        for idx, record in enumerate(records):
            if self.record_limit is not None and idx >= self.record_limit:
                break
            logger.info(f"Processing Record Index: {idx}")
            # clear the shared exception list for this request.
            exceptions.APIException.errors = []

            if not isinstance(record, dict):
                logger.error(
                    f"Error processing invalid record {idx}: expected dict, got {type(record).__name__}.")
                self.summary.add_fail(
                    idx, record, f"Invalid record type: expected dict, got {type(record).__name__}")
                continue

            if not record:
                logger.error(f"Error processing empty record {idx}.")

            # Skip records matching filter value
            if self.skip_urls and record.get('site_url') and self.skip_urls.casefold() in record.get('site_url', '').casefold():
                logger.info(
                    f"Skipping record matching '{self.skip_urls}'. Site URL: '{record.get('site_url')}', Title: '{record.get('title', '?')}'")
                self.summary.add_skip(idx, record)
                continue

            try:
                result = self.transmit_osti_record(record, idx)
            except exceptions.BadRequestException as ve:
                logger.error(
                    f"Error Transmitting new Record: {ve.message}\n{ve.errors}")
                self.summary.add_fail(
                    idx, record, f"{ve.message}\n{ve.errors}")
            except MultipleMatchesError as e:
                self.summary.add_fail(idx, record, f"{repr(e)}")
            except ValueError as e:
                # Catch validation errors (including pydantic ValidationError which inherits from ValueError)
                # This handles Record model validation errors from elinkapi
                error_name = type(e).__name__
                if error_name == 'ValidationError':
                    self.summary.add_fail(
                        idx, record, f"Invalid Record: {repr(e)}")
                else:
                    self.summary.add_fail(
                        idx, record, f"Value error: {repr(e)}")
            except Exception as e:
                self.summary.add_fail(
                    idx, record, f"Unexpected exception transmitting record {repr(e)}")
            else:
                if not result:
                    self.summary.add_fail(
                        idx, record, f"Unknown error: Transmit attempt returned {repr(result)}")

        return self.summary


def _init_api(api_key, api_url):
    token = api_key or os.environ.get('OSTI_API_KEY')
    target = api_url or os.environ.get('OSTI_API_URL')
    if token:
        logger.debug("Initialized with authentication token")
    else:
        logger.warning(
            "No API key provided - some records may not be accessible")
    if target:
        logger.warning(f"Initialized API with custom URL: {target}")
        return Elink(target=target, token=token)
    else:
        return Elink(token=token)
