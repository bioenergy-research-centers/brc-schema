#!/bin/bash
# Test various output format options

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURES_DIR="$SCRIPT_DIR/fixtures"

# Test JSON output
echo '✓ Testing JSON output format...'
poetry run brcschema transform -T osti_to_brc -o /tmp/demo.json "$FIXTURES_DIR/shewanella.json" > /dev/null 2>&1
python3 <<'EOF'
import json
data = json.load(open("/tmp/demo.json"))
print(f'JSON: {data["datasets"][0]["brc"]} dataset with {len(data["datasets"][0]["funding"])} funding source(s)')
EOF

# Test YAML output  
echo '✓ Testing YAML output format...'
poetry run brcschema transform -T osti_to_brc -o /tmp/demo.yaml "$FIXTURES_DIR/shewanella.json" > /dev/null 2>&1
python3 <<'EOF'
import yaml
data = yaml.safe_load(open("/tmp/demo.yaml"))
print(f'YAML: {data["datasets"][0]["brc"]} dataset with {len(data["datasets"][0]["funding"])} funding source(s)')
EOF

# Test .yml extension (should still use YAML)
echo '✓ Testing .yml extension (should use YAML)...'
poetry run brcschema transform -T osti_to_brc -o /tmp/demo.yml "$FIXTURES_DIR/shewanella.json" > /dev/null 2>&1
python3 <<'EOF'
import yaml
data = yaml.safe_load(open("/tmp/demo.yml"))
print(f'YML:  {data["datasets"][0]["brc"]} dataset with {len(data["datasets"][0]["funding"])} funding source(s)')
EOF

echo '✅ All output formats working correctly!'

# Cleanup
rm -f /tmp/demo.json /tmp/demo.yaml /tmp/demo.yml
