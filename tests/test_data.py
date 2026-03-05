"""Validation tests for example data using LinkML tooling."""

import json
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner
from linkml.validator import Validator
from linkml.validator.plugins import JsonschemaValidationPlugin
from linkml.validator.report import Severity

from brc_schema.cli import main

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "src" / "brc_schema" / "schema" / "brc_schema.yaml"
VALID_EXAMPLES_DIR = ROOT / "src" / "data" / "examples" / "valid"
INVALID_EXAMPLES_DIR = ROOT / "src" / "data" / "examples" / "invalid"


def _validation_errors(instance: dict) -> list[str]:
    validator = Validator(
        schema=str(SCHEMA_PATH),
        validation_plugins=[JsonschemaValidationPlugin(closed=True)],
    )
    report = validator.validate(instance, target_class="DatasetCollection")
    return [
        result.message
        for result in report.results
        if result.severity in (Severity.ERROR, Severity.FATAL)
    ]


@pytest.mark.parametrize(
    "path",
    sorted(VALID_EXAMPLES_DIR.glob("*.json")),
    ids=lambda p: p.name,
)
def test_valid_examples_pass_linkml_validation(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = _validation_errors(data)
    assert errors == [], f"Unexpected validation errors for {path.name}: {errors}"


@pytest.mark.parametrize(
    "path",
    sorted(INVALID_EXAMPLES_DIR.glob("*.json")),
    ids=lambda p: p.name,
)
def test_invalid_examples_fail_linkml_validation(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = _validation_errors(data)
    assert errors, f"Expected at least one validation error for {path.name}"


def test_transformed_fixture_validates_against_schema(tmp_path: Path):
    """Mirror validation_test.sh: transform OSTI fixture, then validate BRC output."""
    input_file = ROOT / "tests" / "fixtures" / "2439925.json"
    output_file = tmp_path / "2439925_brc.yaml"

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["transform", "-T", "osti_to_brc", "-o", str(output_file), str(input_file)],
    )

    assert result.exit_code == 0, result.output
    transformed_data = yaml.safe_load(output_file.read_text(encoding="utf-8"))
    assert _validation_errors(transformed_data) == []
