"""Tests for transform module path resolution."""

from brc_schema.transform import set_up_transformer


def test_set_up_transformer_uses_package_relative_paths(monkeypatch, tmp_path):
    """Transformer setup should not depend on the current working directory."""
    monkeypatch.chdir(tmp_path)

    transformer = set_up_transformer("osti_to_brc")

    assert transformer.source_schemaview is not None
    assert transformer.target_schemaview is not None
