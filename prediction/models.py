from django.db import models

# Create your models here.
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
