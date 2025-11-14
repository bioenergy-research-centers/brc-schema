# Scripts

## update_transform_version.py

This script automatically synchronizes the `schema_version` value in the OSTI to BRC transformation config (`src/brc_schema/transform/osti_to_brc.yaml`) with the `version` field in the BRC schema (`src/brc_schema/schema/brc_schema.yaml`).

### Usage

The script is automatically run as part of the `make gen-project` target. It can also be run manually:

```bash
poetry run python scripts/update_transform_version.py
```

### How it works

1. Reads the `version` field from `src/brc_schema/schema/brc_schema.yaml`
2. Updates the `schema_version` expr in `src/brc_schema/transform/osti_to_brc.yaml` to match
3. Prints status messages indicating what was done

### Example

If `brc_schema.yaml` has:
```yaml
version: "0.1.8"
```

Then after running the script, `osti_to_brc.yaml` will have:
```yaml
schema_version:
  expr: '0.1.8'
```

This ensures that when OSTI records are transformed to BRC format, they always reflect the correct schema version being used.
