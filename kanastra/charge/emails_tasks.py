from datetime import datetime
import logging
from django.db import transaction
from django.utils import timezone

from charge.models import Charge

logger = logging.getLogger(__name__)


def send_emails():
    CHUNCK_SIZE = 1000

    with transaction.atomic():
        emails_to_send = Charge.objects.select_for_update().filter(
            email_date__isnull=True
        )[:CHUNCK_SIZE]

        for charge in emails_to_send:
            send_email(charge)
            charge.email_date = timezone.make_aware(datetime.now())
            charge.save()


def send_email(charge: Charge):
    logger.warning("Email sent to " + charge.email)
