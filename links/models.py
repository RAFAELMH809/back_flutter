from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Link(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField(max_length=1000)
    description = models.TextField(blank=True)
