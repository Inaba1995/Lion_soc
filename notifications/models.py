from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ("like", "Like"),
        ("comment", "Comment"),
        ("follow", "Follow"),
        ("message", "Message"),
    ]
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    text = models.CharField(max_length=300)
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.type}] {self.text[:40]}"
