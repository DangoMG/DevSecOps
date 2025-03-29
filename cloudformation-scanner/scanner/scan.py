import os
import subprocess
import json
from datetime import datetime
import argparse
import sys

CRITICAL_CHECKS = {
    "CKV_AWS_21": "S3 Bucket has public read permissions",
    "CKV_AWS_57": "IAM role allows wildcard (*) actions",
}

SEVERITY_PRIORITY = {
    "none": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}

def scan_file(file_path, output_dir):
    output_path = os.path.join(output_dir, os.path.basename(file_path) + "_report.json")
    result = subprocess.run(
        ["checkov", "-f", file_path, "-o", "json"],
        capture_output=True,
        text=True
    )
    with open(output_path, "w") as f:
        f.write(result.stdout)
    return output_path

def summarize_scan(json_file):
    with open(json_file) as f:
        data = json.load(f)

    failed = data.get("summary", {}).get("failed", 0)
    passed = data.get("summary", {}).get("passed", 0)
    critical_hits = []

    for result in data.get("results", {}).get("failed_checks", []):
        check_id = result.get("check_id")
        if check_id in CRITICAL_CHECKS:
            critical_hits.append({
                "check_id": check_id,
                "resource": result.get("resource"),
                "description": CRITICAL_CHECKS[check_id]
            })

    return {
        "file": os.path.basename(json_file).replace("_report.json", ""),
        "passed": passed,
        "failed": failed,
        "critical_issues": critical_hits,
        "raw_issues": data.get("results", {}).get("failed_checks", [])
    }

def write_markdown_summary(reports, output_path):
    with open(output_path, "w") as f:
        f.write("# ☁️ CloudFormation Security Scan Report\n\n")
        f.write("## ✅ Summary Table\n\n")
        f.write("| File | Passed | Failed | Critical Issues |\n")
        f.write("|------|--------|--------|------------------|\n")
        for report in reports:
            f.write(f"| {report['file']} | {report['passed']} | {report['failed']} | {len(report['critical_issues'])} |\n")

        f.write("\n---\n\n")
        f.write("## 🚨 Critical Findings\n\n")
        for report in reports:
            for issue in report['critical_issues']:
                f.write(f"- **{issue['description']}** in `{report['file']}` → `{issue['resource']}` ({issue['check_id']})\n")

def fail_based_on_severity(reports, threshold):
    highest_severity_found = "none"

    for report in reports:
        for issue in report["raw_issues"]:
            severity = issue.get("severity", "low").lower()
            if SEVERITY_PRIORITY[severity] > SEVERITY_PRIORITY[highest_severity_found]:
                highest_severity_found = severity

    if SEVERITY_PRIORITY[highest_severity_found] >= SEVERITY_PRIORITY[threshold]:
        print(f"❌ Failing scan due to '{highest_severity_found}' issue found (threshold: {threshold})")
        sys.exit(1)

def run_scanner(path, output_format, fail_on):
    print(f"\n🔍 Scanning templates in {path}...\n")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    result_dir = os.path.join("cloudformation-scanner", "results", timestamp)
    os.makedirs(result_dir, exist_ok=True)

    scan_summaries = []

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".yaml", ".yml", ".json")):
                full_path = os.path.join(root, file)
                print(f"➡️ Scanning: {file}")
                report_json = scan_file(full_path, result_dir)
                summary = summarize_scan(report_json)
                scan_summaries.append(summary)

    if output_format == "md":
        md_path = os.path.join(result_dir, "scan_summary.md")
        write_markdown_summary(scan_summaries, md_path)
        print(f"\n✅ Markdown report saved to: {md_path}\n")
    else:
        print(json.dumps(scan_summaries, indent=2))

    fail_based_on_severity(scan_summaries, fail_on)

# 🚀 CLI Entry Point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CloudFormation Security Scanner")
    parser.add_argument("--path", type=str, required=True, help="Directory to scan")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="Output format")
    parser.add_argument("--fail-on", choices=["none", "low", "medium", "high", "critical"], default="none", help="Minimum severity to fail CI")

    args = parser.parse_args()
    run_scanner(args.path, args.format, args.fail_on)
