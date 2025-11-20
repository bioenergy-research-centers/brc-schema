"""I/O utilities for brc_schema"""

import logging
import sys
from pathlib import Path
from typing import Any, List, Optional, Union

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


def remove_none_values(data: Any) -> Any:
    """
    Remove None values from dictionaries and lists recursively.

    This function helps create cleaner output by excluding fields that have None values,
    which is especially useful for optional fields that don't have meaningful data.

    :param data: The data to process
    :type data: Any
    :return: Data with None values removed from dictionaries
    :rtype: Any
    """
    if data is None:
        return None

    if isinstance(data, dict):
        # Only include key-value pairs where value is not None
        result = {}
        for key, value in data.items():
            cleaned_value = remove_none_values(value)
            if cleaned_value is not None:
                result[key] = cleaned_value
        return result

    if isinstance(data, list):
        # Remove None values from lists and recursively clean remaining items
        return [remove_none_values(item) for item in data if item is not None]

    # For all other types, return as-is
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
        # Remove None values for cleaner output
        cleaned_data = remove_none_values(sanitized_data)
        text_dump = yaml_dumper.dumps(cleaned_data)
    elif output_format == "json":
        sanitized_data = sanitize_for_yaml(output_data)
        # Remove None values for cleaner output
        cleaned_data = remove_none_values(sanitized_data)
        # Use LinkML's JSON dumper to preserve LinkML-specific structures
        text_dump = json_dumper.dumps(cleaned_data)
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


def read_ids_from_file(file_path: Path) -> List[str]:
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


def convert_json_to_yaml(json_file_path: str, wrap_in_records: bool = True) -> str:
    """
    Convert a JSON file to YAML format, optionally wrapping list data in a records container.

    This is useful for converting OSTI API responses (which may be plain lists) into
    the expected OSTI schema format with a records wrapper.

    Args:
        json_file_path: Path to the input JSON file
        wrap_in_records: If True and data is a list, wraps it in {"records": [...]}

    Returns:
        Path to the newly created YAML file
    """
    import yaml

    # Load JSON data
    with open(json_file_path) as file:
        input_obj = yaml.safe_load(file)

    # Wrap the input in a records container only if it's a plain list
    if wrap_in_records and isinstance(input_obj, list):
        wrapped_obj = {"records": input_obj}
    else:
        # Already wrapped (e.g., {"records": [...]}) or wrapping not requested
        wrapped_obj = input_obj

    # Create output path
    yaml_path = json_file_path.rsplit(".", 1)[0] + ".yaml"

    # Write to YAML file
    with open(yaml_path, "w", encoding="utf-8") as yaml_file:
        yaml.safe_dump(
            data=wrapped_obj,
            stream=yaml_file,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False
        )

    return yaml_path
