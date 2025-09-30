"""CLI for brc_schema"""

import logging
from typing import Any, Optional

import click
import yaml

from brc_schema.transform_osti_to_brc import set_up_transformer
from brc_schema.util.io import dump_output

output_option = click.option("-o", "--output", help="Output file.")
tx_type_option = click.option("-T", "--transform-type", help="Type of transformation. Either 'osti_to_brc' or 'brc_to_osti'.")

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
@output_option
@tx_type_option
@click.option("--source-type")
@click.argument("input_data")
def transform(
    input_data: str,
    source_type: Optional[str],
    tx_type: str,
    output: Optional[str],
    **kwargs: dict[str, Any],
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
    tr.index(input_obj, source_type)
    tr_obj = tr.map_object(input_obj, source_type)
    dump_output(tr_obj, "yaml", output)


if __name__ == "__main__":
    main()
