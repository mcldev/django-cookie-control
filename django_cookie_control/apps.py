from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class CookieControlConfig(AppConfig):
    name = 'django_cookie_control'
    verbose_name = _('Django Cookie Control')

    def ready(self):
        import django_cookie_control.receivers
