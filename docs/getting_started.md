# Getting Started

This repository contains the Bioenergy Research Center (BRC) schema and tooling used to transform and validate metadata exchanged with OSTI E-Link.

- Project site: <https://bioenergy-research-centers.github.io/brc-schema>
- Bioenergy data portal: <https://bioenergy.org/>

## Installation

This repository uses [`uv`](https://docs.astral.sh/uv/) to manage the project environment.
Here, `uv` is responsible for creating `.venv/`, installing dependencies from `pyproject.toml`
and `uv.lock`, and running commands in that environment.

Install `uv` first. The recommended method is:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

You can also install it with `brew install uv`, `pipx install uv`, or `pip install uv`.

Then verify the installation:

```bash
uv --version
```

Finally, sync the project environment:

```bash
uv sync
```

Run CLI commands with `uv run`:

```bash
uv run brcschema --help
```

Or activate the local virtual environment once per shell:

```bash
source .venv/bin/activate
brcschema --help
```

## Repository Layout

- `docs/`: MkDocs documentation sources
- `examples/`: Example inputs and outputs
- `project/`: Generated project artifacts (do not edit directly)
- `src/brc_schema/schema/`: LinkML schema source files
- `src/brc_schema/transform/`: OSTI<->BRC transformation specs
- `src/brc_schema/util/`: I/O, OSTI API, and helper utilities
- `tests/`: Unit and integration tests

## Common Development Commands

- `make install`: install dependencies
- `make gen-project`: regenerate project artifacts and datamodel
- `make gendoc`: regenerate schema reference docs into `docs/`
- `make site`: build project artifacts and docs
- `make test`: run schema and Python tests
- `make testdoc`: regenerate docs and run local MkDocs server
- `make deploy`: deploy docs site

## Quick Workflow

Retrieve OSTI records and transform them into BRC format:

```bash
uv run brcschema retrieve-osti --osti-ids 2584700 --osti-ids 2574191 -o osti_records.json
uv run brcschema transform -T osti_to_brc -o brc_datasets.yaml osti_records.json
```

Transform BRC data back to OSTI format:

```bash
uv run brcschema transform -T brc_to_osti -o osti_records.yaml brc_datasets.yaml
```

## Related Documentation

- [CLI Usage](cli.md)
- [OSTI E-Link Integration](osti_elink_integration.md)
- [Updating the Schema](update_schema.md)
- [Schema Reference](index.md)
