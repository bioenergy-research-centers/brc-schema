#!/bin/bash

echo "=== Running tests WITHOUT OSTI_API_KEY ==="
original_osti_api_key="${OSTI_API_KEY:-}"
unset OSTI_API_KEY
uv run pytest tests/test_elink.py -v --tb=no -q | grep -E "(PASSED|SKIPPED|test_)"

echo ""
echo "=== Summary without API key ==="
uv run pytest tests/test_elink.py --tb=no -q 2>&1 | tail -1

echo ""
echo "=== Running tests WITH OSTI_API_KEY (if set in your environment) ==="
echo "Note: Integration tests will only run if OSTI_API_KEY is available"
if [ -n "$original_osti_api_key" ]; then
    OSTI_API_KEY="$original_osti_api_key" uv run pytest tests/test_elink.py -v --tb=no -q -m integration | grep -E "(PASSED|FAILED|test_)"
else
    echo "OSTI_API_KEY not set - integration tests would be skipped"
fi
