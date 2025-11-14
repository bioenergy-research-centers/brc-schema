#!/usr/bin/env python3
"""
Update the schema_version in osti_to_brc.yaml to match the version in brc_schema.yaml
"""
import re
import sys
from pathlib import Path


def extract_schema_version(schema_path: Path) -> str:
    """Extract version from brc_schema.yaml"""
    content = schema_path.read_text()
    match = re.search(r'^version:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
    if not match:
        raise ValueError(f"Could not find version in {schema_path}")
    return match.group(1)


def update_transform_version(transform_path: Path, version: str) -> None:
    """Update the schema_version expr in osti_to_brc.yaml"""
    content = transform_path.read_text()
    
    # Pattern to match the schema_version expr line
    pattern = r"(      schema_version:\s*\n\s*expr:\s*)['\"].*['\"]"
    replacement = rf"\1'{version}'"
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content == content:
        print(f"Warning: No changes made to {transform_path}", file=sys.stderr)
        return
    
    transform_path.write_text(new_content)
    print(f"Updated schema_version to '{version}' in {transform_path}")


def main():
    # Paths relative to project root
    project_root = Path(__file__).parent.parent
    schema_path = project_root / "src/brc_schema/schema/brc_schema.yaml"
    transform_path = project_root / "src/brc_schema/transform/osti_to_brc.yaml"
    
    # Extract version from schema
    version = extract_schema_version(schema_path)
    print(f"Found schema version: {version}")
    
    # Update transform config
    update_transform_version(transform_path, version)


if __name__ == "__main__":
    main()
