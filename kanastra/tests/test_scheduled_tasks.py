from datetime import datetime
import pytest
import logging

from charge.models import Charge
from charge.emails_tasks import send_emails


@pytest.fixture
def charge_samples(db):
    Charge.objects.create(
        name="Jessica James",
        government_id="5829",
        email="lisa11@example.net",
        debt_amount=1525,
        debt_due_date=datetime.strptime("2024-01-18", "%Y-%m-%d"),
        debt_id="e2dba21b-5520-4226-82b5-90c6bb3356c6",
    )

    Charge.objects.create(
        name="Wyatt Graham",
        government_id="2277",
        email="austinhernandez@example.org",
        debt_amount=5737,
        debt_due_date=datetime.strptime("2024-01-19", "%Y-%m-%d"),
        debt_id="d00318eb-9bb8-4ba8-a4ec-fc80b89d128c",
    )

    Charge.objects.create(
        name="Christopher Adkins",
        government_id="3132",
        email="lauriecantu@example.org",
        debt_amount=5225,
        debt_due_date=datetime.strptime("2024-01-12", "%Y-%m-%d"),
        debt_id="8b0081c1-7cf2-487f-8fbd-3daf2ffc473d",
    )


@pytest.mark.django_db
def test_scheduled_task_send_emails(caplog, charge_samples):

    total_charges = Charge.objects.all().count()
    assert total_charges == 3

    total_emails_sent = Charge.objects.filter(email_date__isnull=False).count()
    assert total_emails_sent == 0

    with caplog.at_level(logging.WARNING):
        send_emails()

    total_emails_sent = Charge.objects.filter(email_date__isnull=False).count()
    assert total_emails_sent == 3

    assert "Email sent to lisa11@example.net" in caplog.text
    assert "Email sent to austinhernandez@example.org" in caplog.text
    assert "Email sent to lauriecantu@example.org" in caplog.text
