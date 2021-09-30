import os
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import FriendList, Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_friend_list(sender, instance, created, **kwargs):
    if created:
        FriendList.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_save)
def remove_unused_media(sender, instance, **kwargs):
    from_fixture = 'raw' in kwargs and kwargs['raw']

    if not from_fixture and sender == Profile:
        profile = sender.objects.filter(pk=instance.pk).first()

        if profile:
            old_image = profile.image
            new_image = instance.image

            path_old = old_image.path.replace("\\", "/")

            if old_image != new_image:
                if settings.MEDIA_DEFAULT_IMAGE not in path_old:
                    os.remove(old_image.path)
