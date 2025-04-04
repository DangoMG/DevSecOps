#!/usr/bin/env python3
import yaml #Make sure this is imported at the top if not already
import os
import subprocess
import json
from datetime import datetime
import argparse
import sys
from remediations import REMEDIATION_LIBRARY
from html_report import generate_html

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

def has_environment_tag(resource_props):
    tags = resource_props.get("Tags", [])
    for tag in tags:
        if tag.get("Key") == "Environment":
            return True
    return False

def no_temp_in_name(resource_props):
    name = resource_props.get("RoleName") or resource_props.get("BucketName") or ""
    return "temp" not in name.lower()

def run_custom_policies(template_file):
    with open(template_file) as f:
        try:
            template = yaml.safe_load(f)
        except:
            return []

    findings = []

    resources = template.get("Resources", {})
    for name, res in resources.items():
        res_type = res.get("Type")
        props = res.get("Properties", {})

        # Custom Rule: Environment tag required
        if not has_environment_tag(props):
            findings.append({
                "resource": name,
                "rule_id": "CUST_TAG_001",
                "message": "Missing required tag: Environment",
                "severity": "medium"
            })

    return findings

def summarize_scan(json_file):
    with open(json_file) as f:
        data = json.load(f)

    failed = data.get("summary", {}).get("failed", 0)
    passed = data.get("summary", {}).get("passed", 0)
    critical_hits = []

    for result in data.get("results", {}).get("failed_checks", []):
        check_id = result.get("check_id")
        details = REMEDIATION_LIBRARY.get(check_id)
        if details:
            critical_hits.append({
                "check_id": check_id,
                "resource": result.get("resource"),
                "title": details["title"],
                "why": details["why"],
                "remediation": details["remediation"],
                "doc": details["doc"]
            })
        else:
            critical_hits.append({
                "check_id": check_id,
                "resource": result.get("resource"),
                "title": result.get("check_name"),
                "why": "No explanation available.",
                "remediation": "Review the rule and secure configuration accordingly.",
                "doc": "https://docs.bridgecrew.io"
            })

    return {
        "file": os.path.basename(json_file).replace("_report.json", ""),
        "passed": passed,
        "failed": failed,
        "critical_issues": critical_hits,
        "raw_issues": data.get("results", {}).get("failed_checks", [])
    }

def run_gitleaks(path, output_dir):
    secrets_file = os.path.join(output_dir, "gitleaks_report.json")
    result = subprocess.run(
        ["gitleaks", "detect", "--source", path, "--report-format", "json", "--report-path", secrets_file],
        capture_output=True,
        text=True
    )
    try:
        with open(secrets_file) as f:
            secrets = json.load(f)
    except json.JSONDecodeError:
        secrets = []
    return secrets

def write_markdown_summary(reports, output_path, secrets):
    with open(output_path, "w") as f:
        f.write("# ☁️ CloudFormation Security Scan Report\n\n")

        # ✅ Summary Table
        f.write("## ✅ Summary Table\n\n")
        f.write("| File | Passed | Failed | Critical Issues | Custom Findings |\n")
        f.write("|------|--------|--------|------------------|-----------------|\n")
        for report in reports:
            f.write(f"| {report['file']} | {report['passed']} | {report['failed']} | {len(report['critical_issues'])} | {len(report.get('custom_findings', []))} |\n")

        f.write("\n---\n\n")

        # 🚨 Critical Findings
        f.write("## 🚨 Critical Findings with Remediation\n\n")
        for report in reports:
            for issue in report['critical_issues']:
                f.write(f"### 🔒 {issue['title']}\n")
                f.write(f"- **File**: `{report['file']}`\n")
                f.write(f"- **Resource**: `{issue['resource']}`\n")
                f.write(f"- **Why it matters**: {issue['why']}\n")
                f.write(f"- **Remediation**: {issue['remediation']}\n")
                f.write(f"- **Docs**: [View]({issue['doc']})\n\n")

        f.write("\n---\n\n")

        # 🧠 Custom Policy Findings
        f.write("## 🧠 Custom Policy Findings\n\n")
        any_custom = False
        for report in reports:
            for finding in report.get("custom_findings", []):
                any_custom = True
                f.write(f"- **[{finding['rule_id']}]** {finding['message']} on resource `{finding['resource']}` (File: `{report['file']}`)\n")
        if not any_custom:
            f.write("No custom policy violations found.\n")

        f.write("\n---\n\n")

        # 🔐 Secrets via Gitleaks
        f.write("## 🔐 Secrets Found (via Gitleaks)\n\n")
        if secrets:
            for s in secrets:
                f.write(f"- **File**: `{s.get('file')}` | **Secret Type**: `{s.get('rule')}` | **Line**: {s.get('line')}, **Commit**: {s.get('commit')[:7]}\n")
        else:
            f.write("No secrets detected.\n")


def fail_based_on_severity(reports, threshold, secrets):
    highest_severity_found = "none"

    for report in reports:
        for issue in report["raw_issues"]:
            raw_severity = issue.get("severity")
            severity = raw_severity.lower() if isinstance(raw_severity, str) else "low"
            if SEVERITY_PRIORITY[severity] > SEVERITY_PRIORITY[highest_severity_found]:
                highest_severity_found = severity

    if secrets:
        print(f"❌ Failing scan due to {len(secrets)} secret(s) detected by Gitleaks.")
        sys.exit(1)

    if SEVERITY_PRIORITY[highest_severity_found] >= SEVERITY_PRIORITY[threshold]:
        print(f"❌ Failing scan due to '{highest_severity_found}' issue found (threshold: {threshold})")
        sys.exit(1)

def get_next_run_dir(base_path):
    today = datetime.now().strftime("%Y_%m_%d")
    i = 1
    while True:
        run_dir = os.path.join(base_path, f"{today}_Run_{i}")
        if not os.path.exists(run_dir):
            return run_dir
        i += 1

def run_scanner(path, output_format, fail_on):
    print(f"\n🔍 Scanning templates in {path}...\n")
    base_results_dir = os.path.join("cloudformation-scanner", "results")
    os.makedirs(base_results_dir, exist_ok=True)
    result_dir = get_next_run_dir(base_results_dir)
    os.makedirs(result_dir, exist_ok=True)

    scan_summaries = []

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".yaml", ".yml", ".json")):
                full_path = os.path.join(root, file)
                print(f"➡ Scanning: {file}")
                report_json = scan_file(full_path, result_dir)
                summary = summarize_scan(report_json)

                # 🔥 Run custom policies (Layer 4)
                custom_findings = run_custom_policies(full_path)
                summary["custom_findings"] = custom_findings

                scan_summaries.append(summary)

    print("\n🔐 Running Gitleaks for secrets scanning...\n")
    secrets = run_gitleaks(path, result_dir)

    # ✅ Always generate HTML report
    html_path = os.path.join(result_dir, "scan_report.html")
    generate_html(scan_summaries, secrets, html_path)
    print(f"✅ HTML report saved to: {html_path}")

    # ✅ Conditionally generate Markdown report
    if output_format == "md":
        md_path = os.path.join(result_dir, "scan_summary.md")
        write_markdown_summary(scan_summaries, md_path, secrets)
        print(f"✅ Markdown report saved to: {md_path}\n")
    elif output_format == "json":
        print(json.dumps({"misconfigs": scan_summaries, "secrets": secrets}, indent=2))

    fail_based_on_severity(scan_summaries, fail_on, secrets)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CloudFormation Security Scanner")
    parser.add_argument("--path", type=str, required=True, help="Directory to scan")
    parser.add_argument("--format", choices=["md", "json", "html"], default="md", help="Preferred terminal output format")
    parser.add_argument("--fail-on", choices=["none", "low", "medium", "high", "critical"], default="none", help="Minimum severity to fail CI")

    args = parser.parse_args()
    run_scanner(args.path, args.format, args.fail_on)
