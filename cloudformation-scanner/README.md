# ☁️ CloudScout – CloudFormation Security Scanner

**CloudScout** is a lightweight, open-source tool that scans AWS CloudFormation templates for misconfigurations and secrets using:

- ✅ [Checkov](https://www.checkov.io/) – for security misconfigurations
- ✅ [Gitleaks](https://github.com/gitleaks/gitleaks) – for hardcoded secrets

It acts like a SAST tool for infrastructure — catching vulnerabilities **before your IaC is deployed**.

---

## 🧠 What It Does

- Scans `.yaml` / `.json` CloudFormation templates
- Flags critical issues like:
  - Public S3 buckets
  - Wildcard IAM permissions
  - Unencrypted resources
- Explains **why it matters** + how to fix it
- Scans for **secrets** like AWS keys, tokens, passwords
- Outputs a clean Markdown report for devs or CI/CD
- Exits with an error code if critical issues or secrets are found

---

## 🚀 Quick Usage

```bash
python cloudformation-scanner/scanner/scan.py \
  --path cloudformation-scanner/templates \
  --format md \
  --fail-on high
