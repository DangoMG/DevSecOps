# ☁️ CloudScout – CloudFormation Security Scanner

**CloudScout** is a lightweight, open-source tool that scans AWS CloudFormation templates for:

- 🔒 Misconfigurations (via [Checkov](https://www.checkov.io/))
- 🕵️ Hardcoded secrets (via [Gitleaks](https://github.com/gitleaks/gitleaks))

It acts like a **SAST tool for Infrastructure as Code**, helping you catch vulnerabilities **before** your templates hit production.

---

## 🧠 What It Does

- ✅ Scans `.yaml` / `.json` CloudFormation templates
- 🚨 Flags critical issues like:
  - Public S3 buckets
  - Wildcard IAM permissions
  - Unencrypted storage
- 🛠️ Provides human-readable explanations & remediation steps
- 🧪 Scans for secrets like AWS keys, tokens, passwords
- 📄 Outputs a Markdown report with severity, context, and fix guidance
- ❌ Exits with non-zero code in CI/CD if issues or secrets are found

---

## ⚡️ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/DangoMG/DevSecOps.git
cd DevSecOps

# 2. (Optional) Make the scanner directly executable
chmod +x cloudformation-scanner/scanner/scan.py

# 3. Run the scanner
python cloudformation-scanner/scanner/scan.py \
  --path cloudformation-scanner/templates \
  --format md \
  --fail-on high
