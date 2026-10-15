import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

# ---------------- CONFIG ----------------
SENDER_EMAIL = "aof.group.auto@gmail.com"
SENDER_NAME = "Business Intelligence"
SENDER_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]

TO = ["o.salahaddin@aofgroup.com"]
CC = ["a.alsalem@aofgroup.com"]

KSA = timezone(timedelta(hours=3))

ARABIC_MONTHS = {
    1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل", 5: "مايو", 6: "يونيو",
    7: "يوليو", 8: "أغسطس", 9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر",
}


def build_message():
    now = datetime.now(KSA)
    month_label = f"{ARABIC_MONTHS[now.month]} {now.year}"

    subject = f"تذكير: تغيير فلاتر الماء لجميع الفروع - {month_label}"

    html = f"""\
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f4f5f7;font-family:Tahoma,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f5f7;padding:24px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" dir="rtl"
             style="background:#ffffff;border-radius:8px;overflow:hidden;border:1px solid #e1e4e8;">
        <tr>
          <td style="background:#1f3a5f;color:#ffffff;padding:20px 24px;font-size:20px;font-weight:bold;text-align:right;">
            تذكير شهري - فريق الصيانة
          </td>
        </tr>
        <tr>
          <td style="padding:24px;font-size:15px;line-height:1.9;color:#222;text-align:right;">
            <p style="margin:0 0 12px;">السلام عليكم ورحمة الله وبركاته،</p>
            <p style="margin:0 0 12px;">
              نود تذكيركم بموعد <strong>تغيير فلاتر الماء لجميع الفروع</strong> لشهر
              <strong>{month_label}</strong>.
            </p>
            <p style="margin:0 0 12px;">
              نرجو التكرم بجدولة الزيارات وإتمام التغيير في جميع الفروع، وإفادتنا عند الانتهاء.
            </p>
            <p style="margin:24px 0 0;">مع خالص التحية،<br></p>
          </td>
        </tr>
        <tr>
          <td style="background:#f8f9fa;color:#888;padding:12px 24px;font-size:12px;text-align:right;">
            .
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
"""

    text = (
        "السلام عليكم ورحمة الله وبركاته،\n\n"
        f"نود تذكيركم بموعد تغيير فلاتر الماء لجميع الفروع لشهر {month_label}.\n"
        "نرجو التكرم بجدولة الزيارات وإتمام التغيير في جميع الفروع، وإفادتنا عند الانتهاء.\n\n"
        "مع خالص التحية،\nإدارة ذكاء الأعمال"
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr((SENDER_NAME, SENDER_EMAIL))
    msg["To"] = ", ".join(TO)
    msg["Cc"] = ", ".join(CC)
    msg.attach(MIMEText(text, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    return msg, subject


def main():
    mode = os.environ.get("MODE", "auto").strip().lower()
    today = datetime.now(KSA)
    print(f"Mode: {mode} | KSA now: {today:%Y-%m-%d %H:%M}")

    if mode != "force" and today.day != 1:
        print("Not the 1st of the month (KSA) - nothing sent.")
        return

    msg, subject = build_message()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, TO + CC, msg.as_string())
    print(f"Sent: {subject}")
    print(f"TO: {TO} | CC: {CC}")


if __name__ == "__main__":
    main()
