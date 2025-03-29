import os
from datetime import datetime
import json


def generate_html(scan_data, secrets_data, output_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>CloudScout Scan Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f7f9fc; }}
        h1 {{ color: #2c3e50; }}
        .summary-table, .findings-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
        .summary-table th, .summary-table td, .findings-table th, .findings-table td {{ border: 1px solid #ddd; padding: 8px; }}
        .summary-table th, .findings-table th {{ background-color: #2c3e50; color: white; }}
        .severity-high {{ color: #e74c3c; font-weight: bold; }}
        .severity-medium {{ color: #f39c12; font-weight: bold; }}
        .severity-low {{ color: #27ae60; font-weight: bold; }}
        .section {{ margin-bottom: 40px; }}
        .collapsible {{ background-color: #3498db; color: white; cursor: pointer; padding: 10px; width: 100%; border: none; text-align: left; outline: none; font-size: 16px; }}
        .active, .collapsible:hover {{ background-color: #2980b9; }}
        .content {{ padding: 0 18px; display: none; overflow: hidden; background-color: #f1f1f1; }}
    </style>
</head>
<body>
    <h1>CloudScout Scan Report</h1>
    <p><strong>Generated:</strong> {timestamp}</p>

    <div class=\"section\">
        <h2>Summary</h2>
        <table class=\"summary-table\">
            <tr><th>File</th><th>Passed</th><th>Failed</th><th>Critical Issues</th></tr>
"""

    for report in scan_data:
        html += f"<tr><td>{report['file']}</td><td>{report['passed']}</td><td>{report['failed']}</td><td>{len(report['critical_issues'])}</td></tr>"

    html += """
        </table>
    </div>

    <div class=\"section\">
        <h2>Critical Findings</h2>
"""

    for report in scan_data:
        for issue in report['critical_issues']:
            html += f"""
            <button class='collapsible'>🔒 {issue['title']} – {issue['resource']}</button>
            <div class='content'>
                <p><strong>File:</strong> {report['file']}</p>
                <p><strong>Why it matters:</strong> {issue['why']}</p>
                <p><strong>Remediation:</strong> {issue['remediation']}</p>
                <p><strong>Docs:</strong> <a href='{issue['doc']}' target='_blank'>{issue['doc']}</a></p>
            </div>
            """

    html += """
    </div>

    <div class=\"section\">
        <h2>Secrets Found</h2>
        <table class=\"findings-table\">
            <tr><th>File</th><th>Line</th><th>Secret Type</th><th>Commit</th></tr>
"""

    if secrets_data:
        for s in secrets_data:
            html += f"<tr><td>{s.get('file')}</td><td>{s.get('line')}</td><td>{s.get('rule')}</td><td>{s.get('commit')[:7]}</td></tr>"
    else:
        html += "<tr><td colspan='4'>No secrets found.</td></tr>"

    html += """
        </table>
    </div>

    <script>
        var coll = document.getElementsByClassName("collapsible");
        for (let i = 0; i < coll.length; i++) {{
            coll[i].addEventListener("click", function() {{
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.display === "block") {{
                    content.style.display = "none";
                }} else {{
                    content.style.display = "block";
                }}
            }});
        }}
    </script>
</body>
</html>
"""

    with open(output_path, "w") as f:
        f.write(html)

    print(f"\n✅ HTML report saved to: {output_path}\n")
