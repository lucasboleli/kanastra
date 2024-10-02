import datetime
import uuid
from django.db import models


class Charge(models.Model):
    name = models.CharField(max_length=255)
    government_id = models.CharField(max_length=255)
    email = models.EmailField()
    debt_amount = models.IntegerField()
    debt_due_date = models.DateField()
    debt_id = models.UUIDField(default=uuid.uuid4, unique=True)
    email_date = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
