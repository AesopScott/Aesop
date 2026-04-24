#!/usr/bin/env python3
"""
notify_registration.py — Email notification after course auto-registration.

Reads aip/registration-report.json (written by add_course.py) and
aip/audit-report.md (written by audit_courses.py), then sends a summary
email to the configured recipient.

Required environment variables:
  NOTIFY_EMAIL_USER   Sender Gmail address (e.g. bot@aesopacademy.org)
  NOTIFY_EMAIL_PASS   Gmail App Password for that account
  NOTIFY_EMAIL_TO     Recipient address (default: ravenshroud@gmail.com)

Usage:
    python .github/scripts/notify_registration.py
"""

import json
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

REPO        = Path(__file__).resolve().parents[2]
REPORT_JSON = REPO / "aip" / "registration-report.json"
AUDIT_MD    = REPO / "aip" / "audit-report.md"
SITE_BASE   = "https://aesopacademy.org"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def load_report() -> dict:
    if not REPORT_JSON.exists():
        print("No registration-report.json found — nothing to notify.")
        sys.exit(0)
    data = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    if not data.get("registered"):
        print("Registration report is empty — no new courses. Skipping notification.")
        sys.exit(0)
    return data


def load_audit_summary() -> str:
    if not AUDIT_MD.exists():
        return "_Audit report not available._"
    text = AUDIT_MD.read_text(encoding="utf-8")
    # Pull just the header + summary section (up to first --- or 40 lines)
    lines = text.splitlines()
    summary_lines = []
    in_summary = False
    for line in lines:
        if line.startswith("## Summary"):
            in_summary = True
        if in_summary:
            summary_lines.append(line)
            if len(summary_lines) > 20:
                break
    return "\n".join(summary_lines) if summary_lines else "\n".join(lines[:30])


def build_html(courses: list[dict], audit_summary: str) -> str:
    course_rows = ""
    for c in courses:
        live_url = f"{SITE_BASE}/ai-academy/modules/{c['id']}/"
        course_rows += f"""
        <tr>
          <td style="padding:10px 12px;border-bottom:1px solid #e2e8f0;">
            <strong>{c['name']}</strong><br>
            <span style="color:#64748b;font-size:13px;">{c['desc'][:120]}{'…' if len(c['desc']) > 120 else ''}</span>
          </td>
          <td style="padding:10px 12px;border-bottom:1px solid #e2e8f0;text-align:center;white-space:nowrap;">
            {c['n_mods']} modules
          </td>
          <td style="padding:10px 12px;border-bottom:1px solid #e2e8f0;">
            <a href="{live_url}" style="color:#6366f1;">View Course →</a>
          </td>
        </tr>"""

    audit_html = audit_summary.replace("\n", "<br>").replace("🟢", "✅").replace("🔴", "❌").replace("🟡", "⚠️")
    n = len(courses)

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
             background:#f8fafc;margin:0;padding:24px;">
  <div style="max-width:680px;margin:0 auto;background:#fff;
              border-radius:12px;overflow:hidden;
              box-shadow:0 1px 3px rgba(0,0,0,.1);">

    <!-- Header -->
    <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);
                padding:32px 36px;color:#fff;">
      <div style="font-size:28px;margin-bottom:4px;">🎓</div>
      <h1 style="margin:0;font-size:22px;font-weight:700;">
        {n} Course{'s' if n != 1 else ''} Now Live on AESOP AI Academy
      </h1>
      <p style="margin:8px 0 0;opacity:.85;font-size:14px;">
        Auto-registration completed successfully
      </p>
    </div>

    <!-- Course list -->
    <div style="padding:28px 36px;">
      <h2 style="margin:0 0 16px;font-size:16px;color:#1e293b;">
        Newly Registered Course{'s' if n != 1 else ''}
      </h2>
      <table style="width:100%;border-collapse:collapse;font-size:14px;color:#334155;">
        <thead>
          <tr style="background:#f1f5f9;">
            <th style="padding:10px 12px;text-align:left;font-weight:600;">Course</th>
            <th style="padding:10px 12px;text-align:center;font-weight:600;">Modules</th>
            <th style="padding:10px 12px;text-align:left;font-weight:600;">Link</th>
          </tr>
        </thead>
        <tbody>{course_rows}
        </tbody>
      </table>
    </div>

    <!-- Audit summary -->
    <div style="padding:0 36px 28px;">
      <h2 style="margin:0 0 12px;font-size:16px;color:#1e293b;">Audit Summary</h2>
      <div style="background:#f8fafc;border-radius:8px;padding:16px;
                  font-size:13px;color:#475569;line-height:1.7;
                  border-left:4px solid #6366f1;">
        {audit_html}
      </div>
    </div>

    <!-- Footer -->
    <div style="background:#f1f5f9;padding:16px 36px;
                font-size:12px;color:#94a3b8;text-align:center;">
      AESOP AI Academy · Auto-registration bot · aesopacademy.org
    </div>

  </div>
</body>
</html>"""


def send_email(subject: str, html_body: str, text_body: str) -> None:
    user    = os.environ.get("NOTIFY_EMAIL_USER")
    passwd  = os.environ.get("NOTIFY_EMAIL_PASS")
    to_addr = os.environ.get("NOTIFY_EMAIL_TO", "ravenshroud@gmail.com")

    if not user or not passwd:
        print("NOTIFY_EMAIL_USER / NOTIFY_EMAIL_PASS not set — skipping email.")
        sys.exit(0)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"AESOP Bot <{user}>"
    msg["To"]      = to_addr
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(user, passwd)
        server.sendmail(user, to_addr, msg.as_string())

    print(f"  ✓ Notification sent to {to_addr}")


def main() -> None:
    report        = load_report()
    courses       = report["registered"]
    audit_summary = load_audit_summary()

    n       = len(courses)
    names   = ", ".join(c["name"] for c in courses)
    subject = f"[AESOP] {n} Course{'s' if n != 1 else ''} Now Live: {names}"

    # Plain-text fallback
    text_body = f"AESOP AI Academy — {n} course(s) registered\n\n"
    for c in courses:
        text_body += f"  • {c['name']} ({c['n_mods']} modules)\n"
        text_body += f"    {SITE_BASE}/ai-academy/modules/{c['id']}/\n\n"
    text_body += f"\nAudit Summary:\n{audit_summary}"

    html_body = build_html(courses, audit_summary)
    send_email(subject, html_body, text_body)


if __name__ == "__main__":
    main()
