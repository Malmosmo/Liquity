from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.utils import timezone
from django.db import models
from django.conf import settings
import os
import shutil
import uuid

from app.models import Group


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


def upload_to(instance, filename):
    return f"profiles/{instance.id}/profile/{filename}"


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default="New User", max_length=16)
    image = models.ImageField(
        default="profile.png",
        upload_to=upload_to
    )
    date = models.DateField(default=timezone.now)
    description = models.TextField(default="Hello, I'm new here.")

    def __str__(self) -> str:
        return f"Profile({self.user.username})"

    def incoming_requests(self):
        in_fq = FriendRequest.objects.filter(receiver=self.user)

        return in_fq.count()

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

        # set name for profile
        if not self.name:
            self.name = self.user.username

        if str(settings.DEFAULT_PROFILE_IMAGE.resolve()) != self.image.path:
            image = Image.open(self.image.path)

            if image.height > 300 or image.width > 300:
                output_size = (300, 300)
                image.thumbnail(output_size)
                image.save(self.image.path)

    def delete(self, *args, **kwargs):
        # group cleanup
        groups = Group.objects.filter(members=self.user)

        for group in groups:
            group.members.remove(self.user)
            group.save()

        groups = Group.objects.filter(creator=self.user)

        for group in groups:
            if group.members.count() > 0:
                group.creator = group.members.first()
                group.members.remove(group.creator)
                group.save()

        # delete user
        self.user.delete()

        # remove profile folder
        path = os.path.join(settings.MEDIA_ROOT, f"profiles/{self.id}")
        if os.path.exists(path):
            shutil.rmtree(path)

        # delete profile
        super().delete(*args, **kwargs)


class FriendList(models.Model):
    # id = models.AutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def __str__(self) -> str:
        return f"FriendList({self.user.username})"

    def add_friend(self, account: User) -> None:
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account: User) -> None:
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee: User) -> None:
        remover_friends_list = self
        remover_friends_list.remove_friend(removee)

        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def delete(self, *args, **kwargs):
        for friend in self.friends:
            self.unfriend(friend)

        super().delete(*args, **kwargs)


class FriendRequest(models.Model):
    # id = models.AutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")

    def __str__(self) -> str:
        return f"FriendRequest({self.sender.username} to {self.receiver.username})"

    def accept(self) -> None:
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)

            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)

                self.delete()

    def decline(self) -> None:
        self.delete()

    def cancel(self) -> None:
        self.delete()
