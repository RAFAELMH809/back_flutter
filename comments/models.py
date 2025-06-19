from django.db import models

# Create your models here.
# comments/models.py
from django.db import models
from django.contrib.auth import get_user_model
from links.models import Link  # Asegúrate de que el modelo Link esté en la app links

User = get_user_model()

class Comment(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} comentó: {self.description[:30]}"
