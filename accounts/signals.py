from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Profile, AppUser


@receiver(post_delete, sender=Profile)
def delete_user_on_profile_delete(sender, instance, **kwargs):

    if instance.user:
        instance.user.delete()


@receiver(post_save, sender=AppUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Създава или обновява профила на потребителя, когато User обект се създава или записва.
    """
    if created:
        # Ако потребителят е новосъздаден, създайте свързан Profile
        Profile.objects.create(user=instance)
    else:
        # Ако потребителят вече съществува, обновете неговия профил
        instance.profile.save()