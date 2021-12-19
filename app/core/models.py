from django.db import models

# Create your models here.
class Member(models.Model):
    mrn = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()

    def __str__(self):
        return f'{self.mrn} - {self.name}'
