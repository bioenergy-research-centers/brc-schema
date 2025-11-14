# Tests Directory

This directory contains all tests for the brc-schema project.

## Structure

- **`fixtures/`** - Reference data files used in tests
  - `2439925.json` - Sample OSTI record
  - `2439925_brc.yaml` - Sample BRC format record
  - `shewanella.json` - Sample OSTI record for Shewanella dataset
  - `shewanella_brc.yaml` - Sample BRC format record for Shewanella

- **Python unit tests:**
  - `test_data.py` - Tests for data validation
  - `test_elink.py` - Tests for OSTI ELINK API integration
  - `test_io.py` - Tests for input/output functionality
  - `test_transforms.py` - Tests for transformation functionality (OSTI ↔ BRC)

- **Integration test scripts:**
  - `test_formats.sh` - Tests various output format options (JSON, YAML, YML)
  - `validation_test.sh` - Validates JSON vs YAML transformation outputs
  - `test_skip_demo.sh` - Tests behavior when OSTI_API_KEY is not set

- **Documentation:**
  - `test_cli_syntax.txt` - Examples of CLI usage patterns

## Running Tests

### Python Unit Tests

Run all Python tests:
```bash
poetry run pytest
```

Run specific test file:
```bash
poetry run pytest tests/test_transforms.py
```

Run with verbose output:
```bash
poetry run pytest -v
```

### Integration Tests

Run format validation test:
```bash
cd tests && ./test_formats.sh
```

Run validation test:
```bash
cd tests && ./validation_test.sh
```

Run OSTI API skip test:
```bash
cd tests && ./test_skip_demo.sh
```

## Notes

- Test scripts automatically use fixture files from the `fixtures/` directory
- Temporary test outputs are written to `/tmp/` to keep the workspace clean
- Python unit tests create their own temporary test data using pytest's `tmp_path` fixture
