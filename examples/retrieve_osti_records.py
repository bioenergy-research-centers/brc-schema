"""Example script demonstrating how to retrieve OSTI records."""

import logging
from pathlib import Path

from brc_schema.util.elink import retrieve_osti_records, OSTIRecordRetriever

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def example_1_simple_retrieval():
    """Example 1: Simple retrieval with convenience function."""
    logger.info("=== Example 1: Simple Retrieval ===")

    # Retrieve records and save to file
    records = retrieve_osti_records(
        osti_ids=[2562995, 2574191],
        dois=["10.1002/aesr.202500034"],
        output_file="osti_records.json"
    )

    logger.info(f"Retrieved {len(records)} records")
    for record in records:
        logger.info(
            f"  - OSTI ID: {record.get('osti_id')}, Title: {record.get('title', 'N/A')[:50]}...")


def example_2_class_based():
    """Example 2: Using the class-based approach."""
    logger.info("\n=== Example 2: Class-based Approach ===")

    # Initialize retriever (optionally with API key)
    retriever = OSTIRecordRetriever()

    # Retrieve individual records
    record1 = retriever.get_record_by_osti_id(2562995)
    if record1:
        logger.info(f"Retrieved record: {record1.get('title', 'N/A')[:50]}...")

    record2 = retriever.get_record_by_doi("10.1002/aesr.202500034")
    if record2:
        logger.info(f"Retrieved record: {record2.get('title', 'N/A')[:50]}...")

    # Retrieve multiple records
    records = retriever.get_records(
        osti_ids=[2574191],
        dois=["10.1021/acscatal.9b02813"]
    )
    logger.info(f"Retrieved {len(records)} records in batch")


def example_3_save_to_file():
    """Example 3: Retrieve and save to specific location."""
    logger.info("\n=== Example 3: Save to Specific File ===")

    retriever = OSTIRecordRetriever()

    output_path = Path("data/osti_downloads/my_records.json")
    num_records = retriever.save_records_to_file(
        output_path=output_path,
        osti_ids=[2562995, 2574191, 1807585],
        pretty=True
    )

    logger.info(f"Saved {num_records} records to {output_path}")


def example_4_read_from_file():
    """Example 4: Read IDs from a file and retrieve."""
    logger.info("\n=== Example 4: Read IDs from File ===")

    # Simulate reading IDs from a file
    osti_ids = [2562995, 2574191, 1807585]
    dois = ["10.1002/aesr.202500034"]

    retriever = OSTIRecordRetriever()
    records = retriever.get_records(osti_ids=osti_ids, dois=dois)

    logger.info(f"Retrieved {len(records)} records from ID list")

    # Process records
    for record in records:
        title = record.get('title', 'N/A')
        osti_id = record.get('osti_id', 'N/A')
        doi = record.get('doi', 'N/A')
        logger.info(f"  - [{osti_id}] {title[:40]}... (DOI: {doi})")


if __name__ == "__main__":
    # Run examples
    try:
        example_1_simple_retrieval()
        example_2_class_based()
        example_3_save_to_file()
        example_4_read_from_file()

        logger.info("\n=== All examples completed successfully ===")

    except Exception as e:
        logger.error(f"Error running examples: {e}", exc_info=True)
