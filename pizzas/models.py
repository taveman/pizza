from django.db import models
from core.models import TimeStampedModel
from django.db.models import QuerySet


class PizzaQuerySet(QuerySet):
    """
    Pizza's QuerySet object with hidden delete method
    """
    def _delete(self):
        super().delete()

    def delete(self):
        for obj in self:
            obj.delete()


class Pizzas(TimeStampedModel):
    """
    Pizza model
    """
    name = models.CharField('Name', max_length=250, null=False)
    is_deleted = models.BooleanField('Is deleted', default=False)

    objects = PizzaQuerySet.as_manager()

    def delete(self, using=None, keep_parents=False):
        """
        Don't delete object from the database
        """
        self.is_deleted = True
        self.save()

    def _delete(self, **kwargs):
        """
        Don't delete object from the database
        """
        super().delete()

    class Meta:
        ordering = ['-created']


class PizzaSizes(TimeStampedModel):
    """
    Pizza size model
    """
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    X_LARGE = 'X'

    SIZE_CHOICES = (
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (X_LARGE, 'X-Large')
    )

    sizename = models.CharField('Size', max_length=1, null=False, unique=True)
    is_deleted = models.BooleanField('Is deleted', default=False)

    objects = PizzaQuerySet.as_manager()

    def delete(self, using=None, keep_parents=False):
        """
        Don't delete object from the database
        """
        self.is_deleted = True
        self.save()

    def create(self):
        """
        Check if we have such a size here and it is active
        """

    class Meta:
        ordering = ['-created']
