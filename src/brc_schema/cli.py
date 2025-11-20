"""CLI for brc_schema"""

import logging
from pathlib import Path
from typing import Optional, List

import click
import yaml

from brc_schema.transform import set_up_transformer, do_transform
from brc_schema.util.io import dump_output, read_ids_from_file, convert_json_to_yaml
from brc_schema.util.elink import OSTIRecordRetriever, OSTIRecordTransmitter

tx_type_option = click.option(
    "-T",
    "--tx-type",
    type=click.Choice(['osti_to_brc', 'brc_to_osti']),
    required=True,
    help="Type of transformation. Either 'osti_to_brc' or 'brc_to_osti'."
)

logger = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", count=True)
def main(verbose: int) -> None:
    """CLI for data manipulation functions in brc_schema."""
    logger = logging.getLogger()
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    logger.info(f"Logger {logger.name} set to level {logger.level}")


@main.command()
@tx_type_option
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    required=True,
    help="Output file path (YAML or JSON, determined by extension)"
)
@click.argument("input_data")
def transform(
    input_data: str,
    tx_type: str,
    output: Path
) -> None:
    """
    Transform input data from OSTI format to BRC schema or vice-versa.

    If input data is not in YAML format, it will be converted to YAML first.

    Output format is determined by the file extension: .json for JSON, otherwise YAML.

    Examples:

        brcschema transform -T osti_to_brc -o data_out_brc_form.yaml data_in_osti_form.yaml

        brcschema transform -T osti_to_brc -o data_out_brc_form.json data_in_osti_form.json

    """
    logger.info(
        f"Transforming {input_data} as {tx_type}"
    )
    tr = set_up_transformer(tx_type)

    # We may need to transform the input data to YAML first
    # If it's in JSON form we may need to wrap it in a records container
    if input_data.endswith(".yaml") or input_data.endswith(".yml"):
        pass
    elif input_data.endswith(".json"):
        input_data = convert_json_to_yaml(input_data)

    with open(input_data, encoding="utf-8") as file:
        input_obj = yaml.safe_load(file)

    if tx_type == "osti_to_brc":
        source_type = "records"
    elif tx_type == "brc_to_osti":
        source_type = "DatasetCollection"
    else:
        raise ValueError(f"Unknown transformation type {tx_type}")

    tr_obj = do_transform(tr, input_obj, source_type)

    # Infer output format from file extension
    output_format = "json" if str(output).endswith(".json") else "yaml"

    dump_output(tr_obj, output_format, str(output))


@main.command()
@click.option(
    "--osti-ids",
    multiple=True,
    help="OSTI ID to retrieve (can be used multiple times)"
)
@click.option(
    "--dois",
    multiple=True,
    help="DOI to retrieve (can be used multiple times)"
)
@click.option(
    "--osti-id-file",
    type=click.Path(exists=True, path_type=Path),
    help="File containing OSTI IDs, one per line"
)
@click.option(
    "--doi-file",
    type=click.Path(exists=True, path_type=Path),
    help="File containing DOIs, one per line"
)
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    required=True,
    help="Output JSON file path"
)
@click.option(
    "--api-key",
    help="OSTI API key (optional, can also use OSTI_API_KEY environment variable)"
)
@click.option(
    "--no-pretty",
    is_flag=True,
    help="Disable pretty-printing of JSON output"
)
def retrieve_osti(
    osti_ids: tuple,
    dois: tuple,
    osti_id_file: Optional[Path],
    doi_file: Optional[Path],
    output: Path,
    api_key: Optional[str],
    no_pretty: bool
) -> None:
    """
    Retrieve records from OSTI E-Link 2.0 API.

    You can provide OSTI IDs, DOIs, or read them from files.
    Retrieved records are saved to a JSON file in OSTI schema format.

    Examples:

        # Retrieve by OSTI IDs (multiple IDs)
        brcschema retrieve-osti --osti-ids 2584700 --osti-ids 2574191 -o records.json

        # Retrieve by DOIs (OSTI format)
        brcschema retrieve-osti --dois 10.11578/2584700 -o records.json

        # Retrieve from ID file
        brcschema retrieve-osti --osti-id-file ids.txt -o records.json

        # Mix of OSTI IDs and DOIs
        brcschema retrieve-osti --osti-ids 2584700 --dois 10.11578/2584700 -o records.json
    """
    # Collect OSTI IDs
    all_osti_ids = list(osti_ids)
    if osti_id_file:
        logger.info(f"Reading OSTI IDs from {osti_id_file}")
        all_osti_ids.extend(read_ids_from_file(osti_id_file))

    # Collect DOIs
    all_dois = list(dois)
    if doi_file:
        logger.info(f"Reading DOIs from {doi_file}")
        all_dois.extend(read_ids_from_file(doi_file))

    # Validate input
    if not all_osti_ids and not all_dois:
        raise click.UsageError(
            "No OSTI IDs or DOIs provided. Use --osti-ids, --dois, "
            "--osti-id-file, or --doi-file"
        )

    logger.info(
        f"Retrieving {len(all_osti_ids)} OSTI IDs and {len(all_dois)} DOIs")

    # Initialize retriever
    retriever = OSTIRecordRetriever(api_key=api_key)

    # Retrieve and save records
    try:
        num_records = retriever.save_records_to_file(
            output_path=output,
            osti_ids=all_osti_ids if all_osti_ids else None,
            dois=all_dois if all_dois else None,
            pretty=not no_pretty
        )

        logger.info(
            f"Successfully saved {len(num_records)} record(s) to {output}")
        click.echo(
            f"✓ Retrieved {len(num_records)} record(s) and saved to {output}")

    except Exception as e:
        logger.error(f"Error retrieving records: {e}", exc_info=True)
        raise click.ClickException(str(e))


@main.command()
@click.option(
    "--api-key",
    help="OSTI API key (optional, can also use OSTI_API_KEY environment variable)"
)
@click.option(
    "--api-url",
    help="OSTI API URL (optional, can also use OSTI_API_URL environment variable. If neither is set, defaults to production URL). For development use: 'https://review.osti.gov/elink2api/'"
)
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Test processing, record validation, and existing data queries without making any persistent changes."
)
@click.option(
    "-n",
    "--new-only",
    is_flag=True,
    help="Only create new records. Do not update existing records found using identifiers."
)
@click.option(
    "--skip-url",
    help="If provided, records with a site_url that contains provided value are skipped and not processed. For example, '--skip-url github'"
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Increase log level to include INFO messages."
)
@click.option(
    "-l",
    "--limit",
    type=int,
    help="Restrict the number of records processed. Combine with --dry-run for testing subsets of data."
)
@click.argument("input_data")
def transmit_osti(
    input_data: str,
    api_key: Optional[str],
    api_url: Optional[str],
    dry_run: bool,
    verbose: bool,
    new_only: bool,
    limit: Optional[int],
    skip_url: Optional[str]
) -> None:
    """
    Transmit input data to OSTI creating new Records.

    If input data is not in YAML format, it will be converted to YAML first.

    Examples:

        brcschema transmit-osti data_in_osti_form.yaml

        brcschema transmit-osti data_in_osti_form.json

    """

    if verbose:
        logging.basicConfig(level=logging.INFO)

    if dry_run:
        logger.warning("Dry-run enabled, no data will be sent.")

    if input_data.endswith(".yaml") or input_data.endswith(".yml"):
        pass
    elif input_data.endswith(".json"):
        input_data = convert_json_to_yaml(input_data)

    with open(input_data, encoding="utf-8") as file:
        input_obj = yaml.safe_load(file)

    if not input_obj['records']:
        logger.error(f"Error processing file. No records found.\n{input_obj}")
    # Initialize transmitter
    transmitter = OSTIRecordTransmitter(
        api_key=api_key, api_url=api_url, dry_run=dry_run)
    # apply options
    if limit:
        transmitter.record_limit = limit
    if skip_url:
        transmitter.skip_urls = skip_url
    if new_only:
        logger.warning(
            "--new-only enabled. Existing records will not be updated.")
        transmitter.new_only = new_only

    summary = transmitter.post_records(input_obj['records'])
    # Output details
    logger.warning(summary.message())

    if summary.fail_count > 0:
        logger.info(
            f"\n=== FAILURE Details ===\n{"\n".join(summary.failures())}")


if __name__ == "__main__":
    main()
