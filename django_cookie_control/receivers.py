from django.db.models.signals import post_save
from .models import CookieControl
from .cache import delete
from django.dispatch import receiver


@receiver(post_save, sender=CookieControl, dispatch_uid="update_cookie_control_clear_cache")
def clear_cookie_cache(sender, instance, **kwargs):
    # Clear the cache
    delete(instance.site_id)



