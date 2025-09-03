"""CLI for brc_schema"""

import logging
from typing import Any, Optional

import click
import yaml
from linkml_map.transformer.object_transformer import ObjectTransformer
from linkml_runtime import SchemaView

from brc_schema.transform_osti_to_brc import set_up_transformer
from brc_schema.util.io import dump_output

output_option = click.option("-o", "--output", help="Output file.")
schema_option = click.option("-s", "--schema", help="Path to source schema.")
transformer_specification_option = click.option(
    "-T", "--transformer-specification", help="Path to transformer specification."
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
@output_option
@schema_option
@click.option("--source-type")
@click.argument("input_data")
def transform(
    input_data: str,
    schema: str,
    source_type: Optional[str],
    transformer_specification: str,
    output: Optional[str],
    **kwargs: dict[str, Any],
) -> None:
    """
    Map data from a source schema to a target schema using a transformation specification.

    Example:
        brcschema transform -T X-to-Y-tr.yaml -s X.yaml  X-data.yaml

    """
    logger.info(
        f"Transforming {input_data} conforming to {schema} using {transformer_specification}"
    )
    tr = ObjectTransformer(**kwargs)
    tr.source_schemaview = SchemaView(schema)
    tr.load_transformer_specification(transformer_specification)
    with open(input_data) as file:
        input_obj = yaml.safe_load(file)
    tr.index(input_obj, source_type)
    tr_obj = tr.map_object(input_obj, source_type)
    dump_output(tr_obj, "yaml", output)


if __name__ == "__main__":
    main()
