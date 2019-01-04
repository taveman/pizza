from django.db import models
from core.models import TimeStampedModel


class Customers(TimeStampedModel):
    """
    Customer model
    """
    FEMALE = 'F'
    MALE = 'M'

    GENDER_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male')
    )

    email = models.EmailField('Email', null=True)
    name = models.CharField('Name', max_length=200, null=False)
    phone = models.CharField('Phone number', max_length=50, null=False)
    age = models.PositiveSmallIntegerField('Age', null=True)
    gender = models.CharField('Gender', max_length=1, choices=GENDER_CHOICES)

    class Meta:
        ordering = ['-created']


