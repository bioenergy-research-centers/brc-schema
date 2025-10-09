"""I/O utilities for brc_schema"""

import logging
import sys
from typing import Any, Optional, Union

from linkml_runtime.dumpers import yaml_dumper, json_dumper

logger = logging.getLogger(__name__)


def sanitize_for_yaml(data: Any, path: str = "root") -> Any:
    """
    Sanitize data structures to ensure they can be serialized to YAML.

    Recursively traverses data structures and replaces any objects that cannot
    be serialized to YAML (like LinkML dynamic objects) with empty strings,
    while logging warnings about what was replaced.

    :param data: The data to sanitize
    :type data: Any
    :param path: The current path in the data structure (for logging), defaults to "root"
    :type path: str
    :return: Sanitized data that can be safely serialized to YAML
    :rtype: Any
    """
    # Handle None, primitives (str, int, float, bool)
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    # Handle lists
    if isinstance(data, list):
        return [sanitize_for_yaml(item, f"{path}[{i}]") for i, item in enumerate(data)]

    # Handle dictionaries
    if isinstance(data, dict):
        return {key: sanitize_for_yaml(value, f"{path}.{key}") for key, value in data.items()}

    # Handle objects that have a representation starting with '<' (like LinkML dynamic objects)
    obj_repr = repr(data)
    if obj_repr.startswith('<') and obj_repr.endswith('>'):
        # This is likely an unparseable object
        logger.warning(
            f"Encountered non-serializable object at {path}: {obj_repr}. "
            f"Type: {type(data).__name__}. Replacing with empty string."
        )
        return ""

    # Try to detect other non-serializable objects
    # Check if it's a custom class instance (not a built-in type)
    if hasattr(data, '__dict__') and not isinstance(data, type):
        logger.warning(
            f"Encountered potential non-serializable object at {path}: {obj_repr}. "
            f"Type: {type(data).__name__}. Replacing with empty string."
        )
        return ""

    # If we get here, try to return the data as-is and let YAML dumper handle it
    # This covers cases like tuples, sets, etc. that might be serializable
    return data


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
    # Sanitize before dumping for either format to avoid dynamic objects
    if output_format == "yaml":
        sanitized_data = sanitize_for_yaml(output_data)
        text_dump = yaml_dumper.dumps(sanitized_data)
    elif output_format == "json":
        sanitized_data = sanitize_for_yaml(output_data)
        # Use LinkML's JSON dumper to preserve LinkML-specific structures
        text_dump = json_dumper.dumps(sanitized_data)
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
