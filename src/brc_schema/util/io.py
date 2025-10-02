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
    Dump output to a file or stdout.

    YAML is preferred.

    :param output_data: data to dump
    :type output_data: dict[str, Any] | list[Any] | str
    :param output_format: format for dumped data, defaults to None
    :type output_format: Optional[str], optional
    :param file_path: path to an output file, defaults to None
    :type file_path: Optional[str], optional
    """

    text_dump = output_data
    if output_format == "yaml":
        text_dump = yaml_dumper.dumps(output_data)
    elif output_format == "str" or output_format is None:
        if isinstance(output_data, str):
            text_dump = output_data
        else:
            text_dump = str(output_data)
    elif output_format and output_format is not None:
        # some other defined output format
        msg = f"Output format {output_format} is not supported"
        raise NotImplementedError(msg)
    else:
        raise ValueError("No output to be printed.")

    if not file_path:
        sys.stdout.write(text_dump)
        return

    with open(file_path, "w", encoding="utf-8") as fh:
        fh.write(text_dump)
