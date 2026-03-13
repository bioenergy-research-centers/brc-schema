"""Tests for transform module path resolution."""

from click.testing import CliRunner

from brc_schema.cli import main
from brc_schema.transform import TransformationError, do_transform, set_up_transformer


def test_set_up_transformer_uses_package_relative_paths(monkeypatch, tmp_path):
    """Transformer setup should not depend on the current working directory."""
    monkeypatch.chdir(tmp_path)

    transformer = set_up_transformer("osti_to_brc")

    assert transformer.source_schemaview is not None
    assert transformer.target_schemaview is not None


class FailingTransformer:
    def map_object(self, input_obj, source_type):
        raise ValueError("bad transform input")


def test_do_transform_raises_exception_instead_of_exiting():
    """Library callers should receive a normal exception on transform failure."""
    transformer = FailingTransformer()

    try:
        do_transform(transformer, {}, "records")
    except TransformationError as e:
        assert "Error during transformation: bad transform input" == str(e)
    else:
        raise AssertionError("Expected TransformationError")


def test_cli_transform_converts_transformation_error_to_click_exception(tmp_path, monkeypatch):
    """CLI should report transformation failures without exposing SystemExit from the library."""
    input_file = tmp_path / "input.yaml"
    output_file = tmp_path / "output.yaml"
    input_file.write_text("records: []\n", encoding="utf-8")

    def fail_transform(*args, **kwargs):
        raise TransformationError(
            "Error during transformation: bad transform input")

    monkeypatch.setattr("brc_schema.cli.do_transform", fail_transform)

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["transform", "-T", "osti_to_brc", "-o",
            str(output_file), str(input_file)],
    )

    assert result.exit_code != 0
    assert "Error during transformation: bad transform input" in result.output
