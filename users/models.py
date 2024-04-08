from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import uuid
# Create your models here.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="profile")
    phone_number = models.TextField(blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return f"Profile of : {self.user}"



class Payment(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

    PAYMENT_STATUS_CHOICES = [
        (PENDING, _('Pending')),
        (COMPLETED, _('Completed')),
        (FAILED, _('Failed')),
    ]
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PENDING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Payment id: {self.transaction_id}"

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
