from __future__ import annotations

import logging
import os
import smtplib
from email.message import EmailMessage

from paper_scout.http import HttpClient

LOGGER = logging.getLogger(__name__)


def send_optional_notifications(markdown: str) -> bool:
    success = True
    webhook_url = os.environ.get("PAPER_SCOUT_WEBHOOK_URL")
    if webhook_url:
        try:
            HttpClient().post_json(webhook_url, {"text": markdown[:3500]})
        except Exception as exc:  # noqa: BLE001 - notifications should not fail the run.
            LOGGER.warning("Webhook notification failed: %s", exc)
            success = False

    smtp_host = os.environ.get("PAPER_SCOUT_SMTP_HOST")
    email_to = os.environ.get("PAPER_SCOUT_EMAIL_TO")
    email_from = os.environ.get("PAPER_SCOUT_EMAIL_FROM")
    if smtp_host and email_to and email_from:
        try:
            message = EmailMessage()
            message["Subject"] = "Paper Scout digest"
            message["From"] = email_from
            message["To"] = email_to
            message.set_content(markdown)
            with smtplib.SMTP(smtp_host, int(os.environ.get("PAPER_SCOUT_SMTP_PORT", "587"))) as smtp:
                if os.environ.get("PAPER_SCOUT_SMTP_STARTTLS", "1") == "1":
                    smtp.starttls()
                if os.environ.get("PAPER_SCOUT_SMTP_USERNAME"):
                    smtp.login(os.environ["PAPER_SCOUT_SMTP_USERNAME"], os.environ.get("PAPER_SCOUT_SMTP_PASSWORD", ""))
                smtp.send_message(message)
        except Exception as exc:  # noqa: BLE001
            LOGGER.warning("Email notification failed: %s", exc)
            success = False
    return success
