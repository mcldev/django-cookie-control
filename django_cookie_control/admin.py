from django.contrib import admin
from django.contrib import messages
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from django_cookie_control.models import *
from django_cookie_control import cache as cookie_cache


# Standard Models
# -----------------
@admin.register(Accessibility, Branding, CallbackFunction, Cookie, iabConfig, ThirdPartyCookie)
class StandardModelAdmin(admin.ModelAdmin):
    pass


# Translated Models
# -----------------
@admin.register(iabText, TextValue)
class TranslatedModelAdmin(TranslatableAdmin):
    form = TranslatableModelForm


# Other Translated Models
# -----------------
@admin.register(Statement, CCPAConfig)
class StatementAdmin(TranslatableAdmin):
    form = TranslatableModelForm
    fieldsets = (
        (None, {
           'fields': ('name', 'url', 'updated', 'description')
        }),
    )

@admin.register(PurposeObject)
class PurposeObjectAdmin(TranslatableAdmin):
    form = TranslatableModelForm
    verbose_name = 'Optional Cookie Control'
    verbose_name_plural = 'Optional Cookie Controls'
    fieldsets = (
        (None, {
           'fields': ('name', 'label', 'description', 'recommendedState', 'lawfulBasis')
        }),
        ('Cookies', {
            'fields': ('cookies', 'thirdPartyCookies')
        }),
        ('Callback Functions', {
            'fields': ('onAccept', 'onRevoke')
        }),
    )



# Optional Cookie Inline..
# -----------------
class OptionalCookieInline(admin.TabularInline):
    model = CookieControl.optionalCookies.through
    verbose_name = 'Optional Cookie'
    verbose_name_plural = 'Optional Cookies'
    extra = 1


class OptionalCookieAdmin(admin.ModelAdmin):
    inlines = [
        OptionalCookieInline,
    ]
    verbose_name = 'Optional Cookie'
    verbose_name_plural = 'Optional Cookies'



# Main Cookie Control Model
# -----------------
@admin.register(CookieControl)
class CookieControlAdmin(admin.ModelAdmin):
    list_editable = ['is_enabled']
    list_display = ['name', 'is_enabled', 'mode', 'iabCMP']
    inlines = [
        OptionalCookieInline,
    ]
    exclude = [
        'optionalCookies',
    ]
    fieldsets = (
        (None, {
           'fields': ('is_enabled', 'site', 'name', 'apiKey', 'product')
        }),
        ('Settings', {
            'classes': ('collapse',),
            'fields': ('consentCookieExpiry', 'statement', 'logConsent', 'encodeCookie', 'subDomains'),
        }),
        ('IAB/CCPA Frameworks', {
            'classes': ('collapse',),
            'fields': ('mode', 'publisherCC', 'iabCMP', 'iabConfig', 'iabText', 'ccpaConfig'),
        }),
        ('Appearance and behaviour', {
            'classes': ('collapse',),
            'fields': ('initialState',
                       'notifyOnce',
                       'rejectButton',
                       'layout',
                       'position',
                       'theme',
                       'toggleType',
                       'acceptBehaviour',
                       'closeOnGlobalChange',
                       'closeStyle',
                       'notifyDismissButton',
                       'settingsStyle',
                       'text',
                       'branding',
                       'excludedCountries',
                       'onLoad',
                       'sameSiteCookie',
                       'sameSiteValue'),
        }),
        ('Accessibility', {
            'classes': ('collapse',),
            'fields': ('accessibility', ),
        }),
        ('Cookies', {
            'fields': ('necessaryCookies', ),
        }),
    )

    def save_model(self, request, obj, form, change):
        super(CookieControlAdmin, self).save_model(request, obj, form, change)
        if obj.is_enabled and CookieControl.objects.filter(site_id=obj.site_id, is_enabled=True).count() > 1:
            messages.add_message(request, messages.WARNING,
                                 'Caution: multiple CookieControls enabled for site: {}'.format(obj.site))




