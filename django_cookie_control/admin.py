from django.contrib import admin
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from django_cookie_control.models import *


# Standard Models
# -----------------
class CookiesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cookie, CookiesAdmin)


class ThirdPartyCookiesAdmin(admin.ModelAdmin):
    pass

admin.site.register(ThirdPartyCookie, ThirdPartyCookiesAdmin)


class CallbackFunctionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(CallbackFunction, CallbackFunctionsAdmin)


class AccessibilityValuesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Accessibility, AccessibilityValuesAdmin)


class BrandingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Branding, BrandingAdmin)


# Translated Models
# -----------------

class StatementAdmin(TranslatableAdmin):
    form = TranslatableModelForm
    fieldsets = (
        (None, {
           'fields': ('name', 'url', 'updated', 'description')
        }),
    )
admin.site.register(Statement, StatementAdmin)


class TextValuesAdmin(TranslatableAdmin):
    form = TranslatableModelForm

admin.site.register(TextValue, TextValuesAdmin)


class PurposeObjectAdmin(TranslatableAdmin):
    form = TranslatableModelForm
    verbose_name = 'Optional Cookie Control'
    verbose_name_plural = 'Optional Cookie Controls'
    fieldsets = (
        (None, {
           'fields': ('name', 'label', 'description')
        }),
        ('Cookies', {
            'fields': ('cookies', 'thirdPartyCookies', 'recommendedState', 'lawfulBasis')
        }),
        ('Callback Functions', {
            'fields': ('onAccept', 'onRevoke')
        }),
    )

admin.site.register(PurposeObject, PurposeObjectAdmin)


# Optional Cookie Inline.. maybe
class OptionalCookieInline(admin.TabularInline):
    model = CookieControl.optionalCookies.through
    verbose_name = 'Optional Cookie'
    verbose_name_plural = 'Optional Cookies'


class OptionalCookieAdmin(admin.ModelAdmin):
    inlines = [
        OptionalCookieInline,
    ]
    verbose_name = 'Optional Cookie'
    verbose_name_plural = 'Optional Cookies'



# Main Cookie Control Model
# -----------------
class CookieControlAdmin(admin.ModelAdmin):
    inlines = [
        OptionalCookieInline,
    ]
    exclude = [
        'optionalCookies',
    ]
    fieldsets = (
        (None, {
           'fields': ('site', 'name', 'apiKey', 'product')
        }),
        ('Display Options', {
            'classes': ('collapse',),
            'fields': ('position', 'theme', 'toggleType', 'closeStyle'),
        }),
        ('Text and Accessibility', {
            'classes': ('collapse',),
            'fields': ('statement', 'text', 'accessibility'),
        }),
        ('Custom Settings', {
            'classes': ('collapse',),
            'fields': ('consentCookieExpiry', 'logConsent', 'notifyOnce', 'onLoad'),
        }),
        ('Pro & Pro_Multisite Settings Only', {
            'classes': ('collapse',),
            'fields': ('initialState', 'layout', 'excludedCountries', 'branding'),
        }),
        ('Cookies', {
            'fields': ('necessaryCookies', ),
        }),
    )

admin.site.register(CookieControl, CookieControlAdmin)



