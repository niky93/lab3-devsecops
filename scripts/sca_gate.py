import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
blocking = []
for dependency in report["dependencies"]:
    for finding in dependency.get("vulnerabilities", []):
        scores = [finding.get(key, {}).get("baseScore", 0) for key in ("cvssv2", "cvssv3", "cvssv4")]
        score = max(float(value or 0) for value in scores)
        if score >= 7:
            blocking.append((dependency["fileName"], finding["name"], score))
print(f"Dependencies: {len(report['dependencies'])}; findings CVSS >= 7: {len(blocking)}")
for filename, name, score in blocking:
    print(f"{filename}: {name} CVSS {score}")
print("Quality Gate FAILED" if blocking else "Quality Gate PASSED")
sys.exit(1 if blocking else 0)
