# ☁️ CloudScout – CloudFormation Security Scanner

**CloudScout** is a lightweight, open-source tool that scans AWS CloudFormation templates for common misconfigurations and security risks.

It uses [Checkov](https://www.checkov.io/) under the hood, and acts like a SAST tool for infrastructure — catching vulnerabilities **before your IaC ever gets deployed**.

---

## 🧠 What It Does

- Scans `.yaml` / `.json` CloudFormation templates
- Flags critical issues like:
  - Public S3 buckets
  - Wildcard IAM permissions
  - Unencrypted resources
- Explains **why the issue matters**
- Provides **remediation guidance** with doc links
- Outputs a Markdown report, suitable for PR reviews and CI pipelines

---

## 🚀 Quick Usage

```bash
python cloudformation-scanner/scanner/scan.py \
  --path cloudformation-scanner/templates \
  --format md \
  --fail-on high
