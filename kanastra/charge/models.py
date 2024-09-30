from django.db import models


class Charge(models.Model):
    name = models.CharField(max_length=50)
    governmentId = models.PositiveIntegerField()
    email = models.EmailField(max_length=254)
    debtAmount = models.PositiveIntegerField()
    debtDueDate = models.DateField(auto_now=False, auto_now_add=False)
    debtId = models.UUIDField(unique=True)
    ticketDate = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    emailDate = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
