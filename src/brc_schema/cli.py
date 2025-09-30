"""CLI for brc_schema"""

import logging
from typing import Any, Optional

import click
import yaml

from brc_schema.transform import set_up_transformer, do_transform
from brc_schema.util.io import dump_output

output_option = click.option("-o", "--output", help="Output file.")
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
@click.argument("input_data")
def transform(
    input_data: str,
    tx_type: str,
) -> None:
    """
    Transform input data from OSTI format to BRC schema or vice-versa.

    If input data is not in YAML format, it will be converted to YAML first.

    Example:

        brcschema transform -T osti_to_brc data_in_osti_form.yaml

    """
    logger.info(
        f"Transforming {input_data} as {tx_type}"
    )
    tr = set_up_transformer(tx_type)
    with open(input_data) as file:
        input_obj = yaml.safe_load(file)

    if tx_type == "osti_to_brc":
        source_type = "records"
    elif tx_type == "brc_to_osti":
        source_type = "DatasetCollection"
    else:
        raise ValueError(f"Unknown transformation type {tx_type}")

    tr_obj = do_transform(tr, input_obj, source_type)
    dump_output(tr_obj, "yaml", "test_output.yaml")


if __name__ == "__main__":
    main()
