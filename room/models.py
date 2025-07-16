from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Rooms(models.Model):
    prediction = models.ForeignKey('prediction.Predictions', models.DO_NOTHING, null=True, blank=True)
    bingoroom = models.ForeignKey('bingo.Bingorooms', models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    close_at = models.DateTimeField(null=True, blank=True)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)

    class Meta:
        managed = True
        unique_together = ('user', 'room')
        db_table = 'adminrooms'

    def __str__(self):
        return f"Admin {self.user.username} de la room {self.room.name}"
