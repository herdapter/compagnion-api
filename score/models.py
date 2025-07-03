from django.db import models
from django.conf import settings
# Create your models here.
class UserScores(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,  # ou CASCADE selon ton besoin
        null=True,  # <-- Ajoute cette option
        blank=True
    )
    room = models.ForeignKey('room.Rooms', models.DO_NOTHING)
    update_at = models.TimeField()

    class Meta:
        managed = True
        db_table = 'user_scores'
