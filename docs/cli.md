# CLI Documentation

The `brcschema` command-line interface provides tools for transforming data between BRC and OSTI schemas, and for interacting with the OSTI E-Link 2.0 API.

## Installation

After installing the package with `poetry install`, the `brcschema` command will be available.

Precede commands with `poetry run`.

## Global Options

All commands support the following global options:

- `-v, --verbose`: Increase verbosity (can be used multiple times: `-v` for INFO, `-vv` for DEBUG)

## Commands

### `transform`

Transform data between OSTI format and BRC schema format.

**Usage:**

```bash
brcschema transform -T <transformation_type> -o <output_file> <input_file>
```

**Options:**

- `-T, --tx-type` **(required)**: Type of transformation
  - `osti_to_brc`: Convert OSTI schema to BRC schema
  - `brc_to_osti`: Convert BRC schema to OSTI schema
- `-o, --output` **(required)**: Output file path (format determined by extension: `.json` or `.yaml`)

**Arguments:**

- `input_data`: Path to input file (JSON or YAML)

**Examples:**

```bash
# Transform OSTI format to BRC schema (YAML output)
brcschema transform -T osti_to_brc -o data_out_brc_form.yaml data_in_osti_form.yaml

# Transform OSTI format to BRC schema (JSON output)
brcschema transform -T osti_to_brc -o data_out_brc_form.json data_in_osti_form.json

# Transform BRC schema to OSTI format
brcschema transform -T brc_to_osti -o data_out_osti_form.yaml data_in_brc_form.yaml
```

**Notes:**

- Input files can be in JSON or YAML format
- JSON input is automatically converted to YAML for processing
- Output format is determined by the file extension

---

### `retrieve-osti`

Retrieve metadata records from the OSTI E-Link 2.0 API using OSTI IDs or DOIs.

**Usage:**

```bash
brcschema retrieve-osti [OPTIONS] -o <output_file>
```

**Options:**

- `--osti-ids`: OSTI ID to retrieve (can be specified multiple times)
- `--dois`: DOI to retrieve (can be specified multiple times)
- `--osti-id-file`: Path to file containing OSTI IDs (one per line)
- `--doi-file`: Path to file containing DOIs (one per line)
- `-o, --output` **(required)**: Output JSON file path
- `--api-key`: OSTI API key (alternatively set `OSTI_API_KEY` environment variable)
- `--no-pretty`: Disable pretty-printing of JSON output

**Examples:**

```bash
# Retrieve by single OSTI ID
brcschema retrieve-osti --osti-ids 2584700 -o records.json

# Retrieve multiple OSTI IDs
brcschema retrieve-osti --osti-ids 2584700 --osti-ids 2574191 -o records.json

# Retrieve by DOI (OSTI format)
brcschema retrieve-osti --dois 10.11578/2584700 -o records.json

# Retrieve from ID file
brcschema retrieve-osti --osti-id-file ids.txt -o records.json

# Mix OSTI IDs and DOIs
brcschema retrieve-osti --osti-ids 2584700 --dois 10.11578/2584700 -o records.json

# With API key
brcschema retrieve-osti --osti-ids 2584700 -o records.json --api-key YOUR_API_KEY
```

**Notes:**

- At least one OSTI ID or DOI must be provided
- You can mix different input methods (command-line options and files)
- Retrieved records are saved in OSTI schema format (JSON)
- API key is optional but may be required for certain records or rate limits

---

### `transmit-osti`

Transmit metadata records to OSTI E-Link 2.0 API, creating new records or updating existing ones.

**Usage:**

```bash
brcschema transmit-osti [OPTIONS] <input_file>
```

**Options:**

- `--api-key`: OSTI API key (alternatively set `OSTI_API_KEY` environment variable)
- `--api-url`: OSTI API URL (alternatively set `OSTI_API_URL` environment variable)
  - Defaults to production URL if not specified
  - For development/testing: `https://review.osti.gov/elink2api/`
- `-d, --dry-run`: Test processing and validation without making persistent changes
- `-n, --new-only`: Only create new records; skip updates to existing records
- `--skip-url`: Skip records containing specified string in `site_url` field
- `-v, --verbose`: Enable INFO-level logging
- `-l, --limit`: Maximum number of records to process (useful for testing)

**Arguments:**

- `input_data`: Path to input file containing records in OSTI format (JSON or YAML)

**Examples:**

```bash
# Basic transmission
brcschema transmit-osti data_in_osti_form.yaml

# Dry run to test without making changes
brcschema transmit-osti --dry-run data_in_osti_form.json

# Only create new records (don't update existing)
brcschema transmit-osti --new-only data_in_osti_form.yaml

# Test with first 10 records only
brcschema transmit-osti --dry-run --limit 10 data_in_osti_form.yaml

# Skip GitHub repositories
brcschema transmit-osti --skip-url github data_in_osti_form.yaml

# Use development API
brcschema transmit-osti --api-url https://review.osti.gov/elink2api/ data_in_osti_form.yaml

# Verbose output with API key
brcschema transmit-osti -v --api-key YOUR_API_KEY data_in_osti_form.yaml
```

**Notes:**

- Input files must contain a `records` key with an array of record objects
- The command checks for existing records using identifiers before creating new ones
- JSON input is automatically converted to YAML for processing
- A summary is displayed showing counts of new, updated, failed, and skipped records
- Failed records are logged with error details

---

## Authentication

Several commands interact with the OSTI E-Link 2.0 API and may require authentication:

### Setting API Key

You can provide the API key in two ways:

1. **Command-line option**: Use `--api-key YOUR_API_KEY`
2. **Environment variable**: Set `OSTI_API_KEY=YOUR_API_KEY`

Example:

```bash
# Using environment variable (recommended for security)
export OSTI_API_KEY="your-api-key-here"
brcschema retrieve-osti --osti-ids 2584700 -o records.json

# Using command-line option
brcschema retrieve-osti --osti-ids 2584700 -o records.json --api-key YOUR_API_KEY
```

### Setting API URL

For testing or development environments:

1. **Command-line option**: Use `--api-url https://review.osti.gov/elink2api/`
2. **Environment variable**: Set `OSTI_API_URL=https://review.osti.gov/elink2api/`

---

## File Formats

### Input Files

The CLI accepts both JSON and YAML formats for input files:

**YAML Example** (`records.yaml`):

```yaml
records:
  - title: "Example Dataset"
    doi: "10.11578/1234567"
    description: "A sample dataset"
    # ... other fields
```

**JSON Example** (`records.json`):

```json
{
  "records": [
    {
      "title": "Example Dataset",
      "doi": "10.11578/1234567",
      "description": "A sample dataset"
    }
  ]
}
```

### ID Files

When using `--osti-id-file` or `--doi-file`, provide one identifier per line:

**Example** (`ids.txt`):

```
2584700
2574191
2573456
```

---

## Workflows

### Complete Workflow: Retrieve, Transform, and Update

```bash
# Step 1: Retrieve records from OSTI
brcschema retrieve-osti --osti-ids 2584700 -o osti_records.json

# Step 2: Transform to BRC schema
brcschema transform -T osti_to_brc -o brc_records.yaml osti_records.json

# Step 3: [Edit brc_records.yaml as needed]

# Step 4: Transform back to OSTI format
brcschema transform -T brc_to_osti -o updated_osti.yaml brc_records.yaml

# Step 5: Test transmission with dry-run
brcschema transmit-osti --dry-run updated_osti.yaml

# Step 6: Transmit to OSTI
brcschema transmit-osti updated_osti.yaml
```

### Batch Processing with Dry Run

```bash
# Test with a small subset first
brcschema transmit-osti --dry-run --limit 5 large_dataset.yaml

# If successful, process all records
brcschema transmit-osti large_dataset.yaml
```

---

## Error Handling

### Common Issues

1. **No records found**: Ensure your input file has a `records` key with an array
2. **Authentication errors**: Verify your API key is correct and has appropriate permissions
3. **Validation errors**: Check that your records conform to the OSTI schema
4. **Multiple matches**: If identifiers match multiple records, the operation will fail for that record

### Debugging

Use verbose mode to see detailed logging:

```bash
# Single verbose flag for INFO level
brcschema -v transmit-osti data.yaml

# Double verbose flag for DEBUG level
brcschema -vv transmit-osti data.yaml
```

Use dry-run mode to test without making changes:

```bash
brcschema transmit-osti --dry-run -v data.yaml
```

## Getting Help

For help with any command:

```bash
# General help
brcschema --help

# Command-specific help
brcschema transform --help
brcschema retrieve-osti --help
brcschema transmit-osti --help
```
