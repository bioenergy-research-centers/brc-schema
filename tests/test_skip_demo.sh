#!/bin/bash

echo "=== Running tests WITHOUT OSTI_API_KEY ==="
unset OSTI_API_KEY
poetry run pytest tests/test_elink.py -v --tb=no -q | grep -E "(PASSED|SKIPPED|test_)"

echo ""
echo "=== Summary without API key ==="
poetry run pytest tests/test_elink.py --tb=no -q 2>&1 | tail -1

echo ""
echo "=== Running tests WITH OSTI_API_KEY (if set in your environment) ==="
echo "Note: Integration tests will only run if OSTI_API_KEY is available"
if [ ! -z "$OSTI_API_KEY" ]; then
    poetry run pytest tests/test_elink.py -v --tb=no -q -m integration | grep -E "(PASSED|FAILED|test_)"
else
    echo "OSTI_API_KEY not set - integration tests would be skipped"
fi
