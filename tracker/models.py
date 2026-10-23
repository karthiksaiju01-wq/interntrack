from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Application(models.Model):
    class Status(models.TextChoices):
        WISHLIST = "wishlist", "Wishlist"
        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    company = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.APPLIED)
    applied_on = models.DateField(default=timezone.localdate)
    job_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_on", "-id"]

    def __str__(self):
        return f"{self.role} at {self.company}"

    def get_absolute_url(self):
        return reverse("tracker:edit", args=[self.pk])
