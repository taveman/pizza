from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract model that provides regular used timestamp fields 'Created' and 'Updated'
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
