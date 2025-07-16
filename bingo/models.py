from django.db import models
from django.conf import settings
# Create your models here.
class UserBingoCases(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    room = models.ForeignKey('room.Rooms', models.DO_NOTHING)
    case_text = models.CharField(max_length=50)
    is_checked = models.BooleanField(default=False)
    position = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'user_bingo_cases'

class ValidatedCases(models.Model):
    bingoroom = models.ForeignKey('Bingorooms', models.DO_NOTHING)
    is_checked = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'validated_cases'

class Bingorooms(models.Model):
    bingo = models.ForeignKey('Bingos', models.DO_NOTHING)
    case_text = models.CharField(max_length=50)
    admin = models.ForeignKey('room.Adminrooms', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'bingorooms'


class Bingos(models.Model):
    case_text = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'bingos'
    def __str__(self):
        return f'Bingo case text {self.case_text}'
