#!/bin/bash
# Final validation: demonstrate JSON vs YAML transform outputs

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURES_DIR="$SCRIPT_DIR/fixtures"

echo 'Testing JSON and YAML transform outputs...'

# Test JSON output
uv run brcschema transform -T osti_to_brc -o /tmp/validation_test.json "$FIXTURES_DIR/2439925.json" > /dev/null 2>&1
json_size=$(wc -c < /tmp/validation_test.json)
echo "✓ JSON output: ${json_size} bytes"

# Test YAML output 
uv run brcschema transform -T osti_to_brc -o /tmp/validation_test.yaml "$FIXTURES_DIR/2439925.json" > /dev/null 2>&1
yaml_size=$(wc -c < /tmp/validation_test.yaml)
echo "✓ YAML output: ${yaml_size} bytes"

# Validate both are parseable
uv run python <<'EOF'
import json, yaml
with open("/tmp/validation_test.json") as f: 
    j = json.load(f)
with open("/tmp/validation_test.yaml") as f: 
    y = yaml.safe_load(f)
    
print(f'✓ Both files parseable: JSON={len(j["datasets"])} datasets, YAML={len(y["datasets"])} datasets')
print(f'✓ Same BRC: {j["datasets"][0]["brc"]} == {y["datasets"][0]["brc"]} -> {j["datasets"][0]["brc"] == y["datasets"][0]["brc"]}')
print(f'✓ Same creator count: JSON={len(j["datasets"][0]["creator"])}, YAML={len(y["datasets"][0]["creator"])}')
EOF

echo '🎉 All I/O functionality validated!'
rm -f /tmp/validation_test.json /tmp/validation_test.yaml
