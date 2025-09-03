"""I/O utilities for brc_schema"""

import sys
from typing import Any, Optional, Union

from linkml_runtime.dumpers import yaml_dumper


def dump_output(
    output_data: Union[dict[str, Any], list[Any], str],
    output_format: Optional[str] = None,
    file_path: Optional[str] = None,
) -> None:
    """
    Dump output as YAML to a file or stdout.

    :param output_data: data to dump
    :type output_data: dict[str, Any] | list[Any] | str
    :param output_format: format for dumped data, defaults to None
    :type output_format: Optional[str], optional
    :param file_path: path to an output file, defaults to None
    :type file_path: Optional[str], optional
    """
    if output_data is None:
        # this should already have been caught...
        msg = "No output to be printed"
        raise ValueError(msg)

    text_dump = output_data
    if output_format == "yaml":
        text_dump = yaml_dumper.dumps(output_data)
    elif output_format:
        # some other defined output format
        msg = f"Output format {output_format} is not supported"
        raise NotImplementedError(msg)

    if not file_path:
        sys.stdout.write(text_dump)
        return

    with open(file_path, "w", encoding="utf-8") as fh:
        fh.write(text_dump)
