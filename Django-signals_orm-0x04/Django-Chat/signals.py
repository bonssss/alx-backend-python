from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id is None:
        return  # New message, no need to log

    try:
        old_instance = Message.objects.get(id=instance.id)
    except Message.DoesNotExist:
        return

    if old_instance.content != instance.content:
        instance.edited = True
        MessageHistory.objects.create(
            message=old_instance,
            old_content=old_instance.content,
        )
