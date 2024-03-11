from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Evento, DateTakenError

@receiver(post_save, sender=Evento)
def handle_evento_save(sender, instance, **kwargs):
    try:
        instance.clean()
    except DateTakenError as e:
        print(f"O agendamento não pôde ser feito: {e.message}")