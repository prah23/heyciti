from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class User(models.Model):
    soeid = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z]{2}\d{5}$',
                message='SOEID must be in the format of 2 letters followed by 5 numbers (e.g., xy60697).'
            )
        ]
    )
    avatar = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.soeid
