# Agent Instructions for `brc-schema`

## Build, test, and lint commands

This repository uses `uv` for environment management. Run project commands with `uv run` unless `.venv` is already activated.

```bash
uv sync
```

Common commands:

```bash
make gen-project   # regenerate generated project artifacts and Python datamodel
make gendoc        # regenerate schema reference docs into docs/
make site          # build generated artifacts and docs
make all           # alias for site
make deploy        # deploy docs/site artifacts
make test          # runs schema generation smoke test plus pytest suite
make lint          # runs linkml-lint on src/brc_schema/schema/brc_schema.yaml
```

Pytest usage:

```bash
uv run pytest tests/ -v
uv run pytest tests/test_cli.py::test_transmit_osti_missing_records_field -q
uv run pytest tests/test_elink.py -m integration -v   # requires OSTI_API_KEY
```

Shell-based integration checks:

```bash
cd tests && ./test_formats.sh
cd tests && ./validation_test.sh
cd tests && ./test_skip_demo.sh
```

Notes:

- CI installs dependencies with `uv sync` and runs `make test`.
- `make lint` currently exits non-zero on existing LinkML naming warnings, so treat it as a schema-style check rather than a clean-pass baseline.

## High-level architecture

- The source of truth is the LinkML schema in `src/brc_schema/schema/`. `brc_schema.yaml` is the xBRC/BRC dataset model used by bioenergy.org, `osti_schema.yaml` models OSTI records, and `brc_repositories.yaml` is imported into the BRC schema.
- This repository is the authoritative schema source for the separate `bioenergy.org` repository. That downstream repo consumes generated JSON schema artifacts from this repo and has its own `AGENT.md` with repo-specific integration guidance.
- `src/brc_schema/cli.py` is the main entrypoint behind `brcschema`. The key commands are `transform`, `retrieve-osti`, `retrieve-osti-site`, and `transmit-osti`.
- OSTI/BRC conversion is split between declarative transform specs in `src/brc_schema/transform/` and helper/inference code in `src/brc_schema/transform.py`. The YAML files define field mappings; `transform.py` handles BRC inference, DOI/contract normalization, person/org reshaping, and package-relative schema loading.
- `src/brc_schema/util/elink.py` wraps three retrieval sources: authenticated E-Link 2.0 JSON, authenticated legacy E-Link 1 XML, and the public OSTI.GOV API. Site-code retrieval intentionally produces a transform-compatible top-level `records` list plus provenance metadata in `retrieval_sources` and `record_origins`.
- `src/brc_schema/util/io.py` owns format conversion and output sanitation. JSON inputs can be wrapped into an OSTI-style `records` container, and YAML/JSON output is cleaned by replacing unserializable LinkML dynamic objects and dropping `None` values.
- Generated artifacts live in `project/` and `src/brc_schema/datamodel/`. They are rebuilt from the schema and transform sources rather than edited directly.
- The normal operational workflow is: retrieve OSTI records as OSTI-schema JSON, then run `brcschema transform -T osti_to_brc ...` to produce a BRC `DatasetCollection`.
- Cross-repo schema rollout is documented in `docs/update_schema.md`. The downstream `bioenergy.org` repo copies this repo's generated JSON schema from `project/jsonschema/brc_schema.schema.json` into its own versioned schema files and controls UI/API support separately.

## Key conventions

- Edit `src/brc_schema/schema/*`, `src/brc_schema/transform/*`, and supporting Python code. Do **not** hand-edit `project/` or `src/brc_schema/datamodel/`; those are generated outputs.
- After changing `brc_schema.yaml` or the transform configs, run `make gen-project`. That target also runs `scripts/update_transform_version.py`, which keeps `src/brc_schema/transform/osti_to_brc.yaml`'s emitted `schema_version` aligned with `src/brc_schema/schema/brc_schema.yaml`.
- If a change affects schema shape, generated JSON schema, or bioenergy.org compatibility, review `docs/update_schema.md` here and the `AGENT.md` in the `bioenergy.org` repository. Keep in mind that `bioenergy.org` may pin schema versions and mark new versions unsupported until its UI catches up.
- Keep wrapper shapes straight when changing transforms or CLI behavior:
  - OSTI-side collections use a top-level `records` list.
  - BRC-side collections use `DatasetCollection` with `datasets`.
  - `retrieve-osti-site` keeps `records` plus provenance metadata so the result can be transformed without losing source information.
- `retrieve-osti` and `retrieve-osti-site` outputs are intentionally transform-ready; preserve the top-level `records` shape when changing retrieval code.
- OSTI DOI retrieval only works for OSTI-style DOIs with the `10.11578/...` prefix. Non-OSTI DOIs are skipped rather than resolved.
- For `--osti-id-file` and `--doi-file`, inputs are one identifier per line and lines starting with `#` are treated as comments.
- Example validation is part of schema work. Valid and invalid examples live under `src/data/examples/`, and CONTRIBUTING expects invalid examples to be invalid for one specific reason.
- Existing tests favor `pytest`, `click.testing.CliRunner`, `tmp_path`, and direct utility/helper assertions. Follow those patterns for new coverage.
