import os

from django_measurement.models import MeasurementField
from measurement.measures import Volume
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.conf import settings


def upload_to(instance, filename):
    return f"profiles/{instance.creator.profile.token}/beer/{filename}"


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="creator"
    )
    name = models.CharField(max_length=64)
    members = models.ManyToManyField(User, related_name="group_member")

    def __str__(self) -> str:
        return f"Group({self.name}, {self.creator.username})"


class Beer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(
        default="default_beer.png",
        upload_to=upload_to
    )

    # unused
    percent = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        default=0.0
    )

    # unused
    description = models.TextField(null=True)

    # unused
    type = models.CharField(max_length=100, default="")

    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def delete(self, *args, **kwargs) -> None:
        if not settings.MEDIA_DEFAULT_BEER in self.image.path:
            os.remove(self.image.path)

        super().delete(*args, **kwargs)


class Drink(models.Model):
    id = models.AutoField(primary_key=True)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    count = models.IntegerField()
    volume = MeasurementField(measurement=Volume, default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Drink({self.beer}, {self.user.username})"
