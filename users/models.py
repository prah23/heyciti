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
    full_name = models.CharField(max_length=255, null=True, blank=True) 
    avatar = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    grade = models.CharField(
        max_length=3,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]\d{2}$',
                message='Grade must be in the format of 1 letter followed by 2 digits (e.g., C05, C10).'
            )
        ],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.soeid
