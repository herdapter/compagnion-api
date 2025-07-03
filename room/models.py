from django.db import models
from django.conf import settings

# Create your models here.
class Rooms(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,  # ou CASCADE selon ton besoin
        null=True,  # <-- Ajoute cette option
        blank=True
    )
    prediction = models.ForeignKey('prediction.Predictions', models.DO_NOTHING)
    bingoroom = models.ForeignKey('bingo.Bingorooms', models.DO_NOTHING)
    admin = models.ForeignKey('room.Adminrooms', models.DO_NOTHING)
    created_at = models.DateField()
    close_at = models.DateField()
    statuschoice = [
        ("en cours", "en cours"),
        ("terminé", "terminé"),
        ("annulé", "annulé"),
    ]
    status = models.CharField(max_length=50, choices=statuschoice, default="en cours")
    name = models.CharField(max_length=50, default="")
    img_team1 = models.CharField(max_length=50, default="")
    img_team2 = models.CharField(max_length=50, default="")
    score_team1 = models.IntegerField(default=0)
    score_team2 = models.IntegerField(default=0)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='RoomMembership',
        related_name='rooms_joined'
    )

    class Meta:
        managed = True
        db_table = 'rooms'


class RoomMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'room')

class Adminrooms(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,  # ou CASCADE selon ton besoin
        null=True,  # <-- Ajoute cette option
        blank=True
    )
    class Meta:
        managed = True
        db_table = 'adminrooms'
