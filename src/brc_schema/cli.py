"""CLI for brc_schema"""

import logging
from pathlib import Path
from typing import Optional, List

import click
import yaml

from brc_schema.transform import set_up_transformer, do_transform
from brc_schema.util.io import dump_output
from brc_schema.util.elink import OSTIRecordRetriever

tx_type_option = click.option(
    "-T",
    "--tx-type",
    required=True,
    help="Type of transformation. Either 'osti_to_brc' or 'brc_to_osti'."
)

logger = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
def main(verbose: int, quiet: bool) -> None:
    """CLI for data manipulation functions in brc_schema."""
    logger = logging.getLogger()
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)
    logger.info(f"Logger {logger.name} set to level {logger.level}")


@main.command()
@tx_type_option
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    required=True,
    help="Output YAML file path"
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

    Example:

        brcschema transform -T osti_to_brc -o data_out_brc_form.yaml data_in_osti_form.yaml

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
        # convert JSON to YAML
        with open(input_data) as file:
            input_obj = yaml.safe_load(file)
        # Wrap the input in a records container only if it's a plain list
        if isinstance(input_obj, list):
            wrapped_obj = {"records": input_obj}
        else:
            # Already wrapped (e.g., {"records": [...]})
            wrapped_obj = input_obj
        yaml_path = input_data.rsplit(".", 1)[0] + ".yaml"
        with open(yaml_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(wrapped_obj, yaml_file)
        input_data = yaml_path

    with open(input_data) as file:
        input_obj = yaml.safe_load(file)

    if tx_type == "osti_to_brc":
        source_type = "records"
    elif tx_type == "brc_to_osti":
        source_type = "DatasetCollection"
    else:
        raise ValueError(f"Unknown transformation type {tx_type}")

    tr_obj = do_transform(tr, input_obj, source_type)
    dump_output(tr_obj, "yaml", str(output))


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
        all_osti_ids.extend(_read_ids_from_file(osti_id_file))

    # Collect DOIs
    all_dois = list(dois)
    if doi_file:
        logger.info(f"Reading DOIs from {doi_file}")
        all_dois.extend(_read_ids_from_file(doi_file))

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

        logger.info(f"Successfully saved {num_records} records to {output}")
        click.echo(f"✓ Retrieved {num_records} records and saved to {output}")

    except Exception as e:
        logger.error(f"Error retrieving records: {e}", exc_info=True)
        raise click.ClickException(str(e))


def _read_ids_from_file(file_path: Path) -> List[str]:
    """
    Read IDs (OSTI IDs or DOIs) from a file, one per line.

    Lines starting with # are treated as comments and ignored.

    Args:
        file_path: Path to file containing IDs

    Returns:
        List of IDs (as strings)
    """
    with open(file_path, 'r') as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith('#')
        ]


if __name__ == "__main__":
    main()
