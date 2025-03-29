# ☁️ CloudFormation Security Scanner

Scans AWS CloudFormation templates for common security issues using [Checkov](https://www.checkov.io/).
This is for IaC scanning for prelim scanning during development to find vulnerabilities (SAST, if you will!)

## 🔧 Usage

```bash
python scanner/scan.py

```
--------------------
--- Installation ---
--------------------
1) Download into Linux <CLI > https://{token}@github.com/DangoMG/DevSecOps.git>
3) Install Checkv <CLI > pip install checkov>
4) Install Rust <CLI > curl https://sh.rustup.rs -sSf | sh>
5) Verify Rust Installed <CLI > source $HOME/.cargo/env>
6) Use <CLI > python3 -m venv venv>
7) Then, <CLI > source venv/bin/activate>
8) Then, Install Dependencies <CLI > pip install -r ~/DevSecOps/cloudformation-scanner/requirements.txt>
9) Change Dirs to DevSecOps <CLI > ~/DevSecOps>
10) Use Scanner (Copy + Paste Below)
11) <CLI > python cloudformation-scanner/scanner/scan.py \
  --path cloudformation-scanner/templates \
  --format md \
  --fail-on high
12) Check Results <CLI > cd ~/DevSecOps/cloudformation-scanner/results/{output_file}

Good Luck!
