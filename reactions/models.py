from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from links.models import Link  # ✅ Correcto

User = get_user_model()

class Reaction(models.Model):
    description = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.description

class BoatLinkReaction(models.Model):
    reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('link', 'user')  # Un usuario no puede reaccionar 2 veces al mismo link
