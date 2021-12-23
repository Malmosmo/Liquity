import os
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.conf import settings

# from users.models import User


def upload_to(instance, filename):
    return f"profiles/{instance.creator.profile.id}/drinks/{filename}"


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(to="users.User", on_delete=models.CASCADE, related_name="creator")
    name = models.CharField(max_length=64)
    members = models.ManyToManyField("users.User", related_name="group_member")

    def __str__(self) -> str:
        return f"Group({self.name}, {self.creator.username})"


class Drink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    image = models.ImageField(
        default="default_drink.png",
        upload_to=upload_to
    )

    creator = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def delete(self, *args, **kwargs) -> None:
        if not settings.MEDIA_DEFAULT_DRINK in self.image.path:
            os.remove(self.image.path)

        super().delete(*args, **kwargs)


class DrinkEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drinkType = models.ForeignKey(Drink, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    count = models.IntegerField()
    volume = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        default=0.5
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"DrinkEntry({self.drinkType}, {self.user.username})"
