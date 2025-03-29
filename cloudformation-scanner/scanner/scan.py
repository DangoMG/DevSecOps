import subprocess
import os
import json

def print_summary(json_path):
    with open(json_path) as f:
        data = json.load(f)
        failed = data.get("summary", {}).get("failed", 0)
        passed = data.get("summary", {}).get("passed", 0)
        print(f"\n📊 Summary:")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")

def run_checkov(template_path):
    print(f"🔍 Scanning {template_path} with Checkov...\n")
    result = subprocess.run(
        ["checkov", "-f", template_path, "-o", "json"],
        capture_output=True,
        text=True
    )

    output_path = os.path.join("cloudformation-scanner", "results", "scan_report.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(result.stdout)

    print("✅ Scan complete. Results saved to", output_path)

if __name__ == "__main__":
    run_checkov("cloudformation-scanner/templates/insecure-s3.yaml")
