import json
import sys
from pathlib import Path

try:
    report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    findings = report["results"]
    errors = report["errors"]
    blocking = [item for item in findings if item["extra"]["severity"] == "ERROR"]
except (OSError, ValueError, KeyError, TypeError) as exc:
    print(f"Quality Gate FAILED: missing or invalid report: {exc}")
    sys.exit(1)

print(f"Findings: {len(findings)}; blocking ERROR: {len(blocking)}; analysis errors: {len(errors)}")
for item in blocking:
    print(f"{item['path']}:{item['start']['line']} - {item['check_id']}")
if blocking or errors:
    print("Quality Gate FAILED: blocking findings or analysis errors")
    sys.exit(1)
print("Quality Gate PASSED")
