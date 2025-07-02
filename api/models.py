# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings

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

class Bingorooms(models.Model):
    bingo = models.ForeignKey('Bingos', models.DO_NOTHING)
    case_text = models.CharField(max_length=50)
    admin = models.ForeignKey(Adminrooms, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'bingorooms'


class Bingos(models.Model):
    case_text = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'bingos'

class Extendusers(models.Model):
    token = models.CharField(max_length=50)
    img = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        null=True,  # <-- Ajoute cette option
        blank=True # ou CASCADE selon ton besoin
    )
    room_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'extendusers'


class Predictions(models.Model):
    question = models.CharField(max_length=50)
    respons = models.CharField(max_length=50)
    start_at = models.TimeField()
    end_at = models.TimeField()
    status = models.CharField(max_length=50)
    timer = models.TimeField()
    is_validated = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'predictions'


class Rooms(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,  # ou CASCADE selon ton besoin
        null=True,  # <-- Ajoute cette option
        blank=True
    )
    prediction = models.ForeignKey(Predictions, models.DO_NOTHING)
    bingoroom = models.ForeignKey(Bingorooms, models.DO_NOTHING)
    admin = models.ForeignKey(Adminrooms, models.DO_NOTHING)
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

    class Meta:
        managed = True
        db_table = 'rooms'


class UserBingoCases(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,  # ou CASCADE selon ton besoin
        null=True,  # <-- Ajoute cette option
        blank=True
    )
    room = models.ForeignKey(Rooms, models.DO_NOTHING)
    case_text = models.CharField(max_length=50)
    is_checked = models.BooleanField()
    position = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'user_bingo_cases'


class UserScores(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,  # ou CASCADE selon ton besoin
        null=True,  # <-- Ajoute cette option
        blank=True
    )
    room = models.ForeignKey(Rooms, models.DO_NOTHING)
    update_at = models.TimeField()

    class Meta:
        managed = True
        db_table = 'user_scores'


class Users(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'users'


class ValidatedCases(models.Model):
    bingoroom = models.ForeignKey(Bingorooms, models.DO_NOTHING)
    is_checked = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'validated_cases'
