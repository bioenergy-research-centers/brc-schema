# OSTI E-Link Integration

This project includes both CLI commands and Python utilities for working with the OSTI E-Link 2.0 API.

## Supported Identifier Formats

- OSTI IDs: `2584700`
- OSTI DOIs: `10.11578/2584700`

Only OSTI-style DOIs (`10.11578/...`) can be resolved by the retriever. Non-OSTI DOI formats are skipped with a warning.

## Authentication

Some records require authentication.

You can provide an API key with any of these methods:

1. Environment variable (recommended):

   ```bash
   export OSTI_API_KEY="your_api_key_here"
   ```

2. CLI option:

   ```bash
   uv run brcschema retrieve-osti --api-key "your_api_key_here" --osti-ids 2584700 -o records.json
   ```

3. Python API:

   ```python
   from brc_schema.util.elink import OSTIRecordRetriever

   retriever = OSTIRecordRetriever(api_key="your_api_key_here")
   ```

## CLI Examples

Use `uv run` (or activate `.venv`) for commands below.

Retrieve by OSTI IDs:

```bash
uv run brcschema retrieve-osti --osti-ids 2584700 --osti-ids 2574191 -o records.json
```

Retrieve by DOI:

```bash
uv run brcschema retrieve-osti --dois 10.11578/2584700 -o records.json
```

Read IDs from files:

```bash
uv run brcschema retrieve-osti --osti-id-file ids.txt -o records.json
uv run brcschema retrieve-osti --doi-file dois.txt -o records.json
```

Mix OSTI IDs and DOIs:

```bash
uv run brcschema retrieve-osti --osti-ids 2584700 --dois 10.11578/2584700 -o records.json
```

Retrieve by BRC/site code from the default sources for the credentials available in the environment:

```bash
uv run brcschema retrieve-osti-site --site-code GLBRC -o glbrc_records.json
```

With no authentication, this command warns and uses only the public OSTI.GOV records API, which can return only public/released records. E-Link 2.0 retrieval requires `OSTI_API_KEY`, and legacy E-Link 1 retrieval requires `OSTI_LEGACY_USERNAME` plus `OSTI_LEGACY_PASSWORD`.

Restrict retrieval to one source API when needed:

```bash
uv run brcschema retrieve-osti-site --site-code GLBRC --source legacy --legacy-username "$OSTI_LEGACY_USERNAME" --legacy-password "$OSTI_LEGACY_PASSWORD" -o glbrc_legacy.json
uv run brcschema retrieve-osti-site --site-code GLBRC --source elink2 -o glbrc_elink2.json
uv run brcschema retrieve-osti-site --site-code GLBRC --source public -o glbrc_public.json
```

The site-code output includes `records` plus `retrieval_sources` and `record_origins`. `record_origins` identifies the source API and origin schema for each record index, such as `osti_elink1_xml` for legacy E-Link 1 records, `osti_public_api_v1_json` for public OSTI.GOV records, and `osti_elink2_json` for E-Link 2.0 records.

## Python API Examples

### Convenience Function

```python
from brc_schema.util.elink import retrieve_osti_records

records = retrieve_osti_records(
    osti_ids=[2584700, 2574191],
    dois=["10.11578/2584700"],
    output_file="osti_records.json"
)

print(f"Retrieved {len(records)} records")
```

### Class-Based Usage

```python
from brc_schema.util.elink import OSTIRecordRetriever

retriever = OSTIRecordRetriever()  # reads OSTI_API_KEY from environment if present

record = retriever.get_record_by_osti_id(2584700)
record_by_doi = retriever.get_record_by_doi("10.11578/2584700")

records = retriever.get_records(
    osti_ids=[2584700, 2574191],
    dois=["10.11578/2584700"]
)

retriever.save_records_to_file(
    output_path="output/osti_records.json",
    osti_ids=[2584700, 2574191],
    pretty=True
)
```

## Reading IDs from Text Files

For `--osti-id-file` and `--doi-file`, use one identifier per line. Blank lines and lines starting with `#` are ignored.

Example `ids.txt`:

```text
# OSTI IDs
2584700
2574191
```

## Output Format

Retrieved records are written in OSTI-schema-style JSON:

```json
{
  "records": [
    {
      "osti_id": "2584700",
      "title": "Example Dataset Title"
    }
  ]
}
```

## Related Pages

- [CLI Usage](cli.md)
- [OSTI to/from xBRC Conversion](osti_xbrc_conversion.md)
- [Updating the Schema](update_schema.md)

## References

- [OSTI E-Link 2.0 API documentation](https://www.osti.gov/elink2api/)
