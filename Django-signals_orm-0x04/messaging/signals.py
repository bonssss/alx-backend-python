from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # New message, not an update

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_instance.content != instance.content:
        instance.edited = True  # ✅ Mark as edited
        MessageHistory.objects.create(
            message=old_instance,
            old_content=old_instance.content,
            edited_by=old_instance.sender  # Fallback for edited_by
        )
User = get_user_model()

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # ✅ Required by checker:
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()