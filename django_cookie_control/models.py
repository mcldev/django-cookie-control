from colorfield.fields import ColorField
from django.contrib.sites.models import Site
from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from filer.fields.image import FilerImageField
from parler.models import TranslatableModel, TranslatedFields

from .settings import *


# Main Application
# -------------------------
# https://www.civicuk.com/cookie-control/v8/documentation


#  Util Functions
# -------------------------
def parse_model(instance, fields=None, exclude=None):
    dict = model_to_dict(instance, fields, exclude)
    if hasattr(instance, '_get_translated_model'):
        dict.update(model_to_dict(instance._get_translated_model(use_fallback=True)))

    dict = {k: v for k, v in dict.items() if v}
    return dict


def parse_sub_model(sub_model_objs):
    return [sub.get_dict() for sub in sub_model_objs]


# Models
# -------------------------
class Cookie(models.Model):
    name = models.CharField(max_length=512, unique=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def get_dict(self):
        return str(self)

    class Meta:
        ordering = ['name']


class ThirdPartyCookie(models.Model):
    name = models.CharField(max_length=512)
    optOutLink = models.URLField(help_text=_('Opt-out Link for third-party cookies'))

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def get_dict(self):
        return parse_model(self)

    class Meta:
        ordering = ['name']


class CallbackFunction(models.Model):
    automated_prefix = models.CharField(max_length=512, null=True, blank=True)
    function_text = models.TextField(help_text=_('JavaScript function, e.g. "function () {...}" '), null=True,
                                     blank=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        if self.automated_prefix:
            return "Attribute Prefix: " + self.automated_prefix

        return "Custom Function: " + self.function_text[:30]

    def get_dict(self, enable=True):
        func_text = ""
        if self.automated_prefix:
            prefix = '' if self.automated_prefix == "*" else self.automated_prefix
            if enable:
                func_text = "function() { enableCookies('" + prefix + "'); }"
            else:
                func_text = "function() { disableCookies('" + prefix + "'); }"
        elif self.function_text:
            func_text = self.function_text

        if func_text:
            func_text = func_text.replace("\n", " ").replace("\r", "")
            return FUNC_START_STR + func_text + FUNC_END_STR


class Statement(TranslatableModel):
    translations = TranslatedFields(

        # The text that you wish to call your terms by, for example Privacy Statement.
        name=models.CharField(max_length=255),

        # The text description that introduces your privacy statement.
        # string
        description=models.TextField(help_text=_('Text introducing the privacy statement'), null=True, blank=True),

    )
    # The URL where your terms may be accessed. This link will try to open in a new tab, so it may point to a PDF document without closing the user's access to your site.
    url = models.CharField(help_text=_('URL where your terms may be accessed'), max_length=512, null=True, blank=True)

    # The date that your privacy statement was last issued, in the format of dd/mm/yyyy.
    updated = models.DateField(help_text=_('Terms updated date'), null=True, blank=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def get_dict(self):
        dict = parse_model(self)
        dict['updated'] = self.updated.strftime('%d/%m/%Y')
        return dict


# Optional Cookies
class PurposeObject(TranslatableModel):
    translations = TranslatedFields(
        # A unique identifier for the category
        name=models.CharField(_('A Unique identifier for the category'), max_length=255),

        # The descriptive title assigned to the category and displayed by the module.
        label=models.CharField(help_text=_('Descriptive Title'), max_length=512, null=True, blank=True),

        # The full description assigned to the category and displayed by the module.
        description=models.TextField(help_text=_('Text introducing the privacy statement'), null=True, blank=True),
    )

    # The name of the cookies that you wish to protect after a user opts in.
    # Note that you can use the * wildcard at the end of the name, if want to define more than one cookies that share the same prefix.
    cookies = models.ManyToManyField(Cookie, blank=True)

    # Only applicable if the category will set third party cookies on acceptance.
    thirdPartyCookies = models.ManyToManyField(ThirdPartyCookie, blank=True)

    # Callback function that will fire on user's opting into this cookie category.
    onAccept = models.ForeignKey(CallbackFunction, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='accept_function')

    onRevoke = models.ForeignKey(CallbackFunction, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='revoke_function')

    # Defines whether or not this category should be accepted (opted in) as part of the user granting consent to the site's recommended settings.
    # boolean false
    recommendedState = models.NullBooleanField(help_text=_('Should category be accepted (opted in)'), null=True,
                                               blank=True)

    # Defines whether this category requires explicit user consent, or if the category can be toggled on prior to any
    #  user interaction and justified under the more flexible lawful basis for processing: legitimate interest.
    # Possible values are either consent or legitimate interest. If you choose to rely on legitimate interest,
    # you are taking on extra responsibility for considering and protecting peoples rights and interests; and must
    # include details of your legitimate interests in your privacy statement. Read more from the ICO
    lawfulBasis = models.CharField(help_text=_('requires explicit user consent'), max_length=255,
                                   choices=COOKIE_CONTROL_LAWFUL_BASIS_CHOICES, null=True, blank=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        # language = get_current_language()
        # return self.known_translation_getter('name', default=None, language_code=language, any_language=True)[0]
        return self.name

    def get_dict(self):
        dict = parse_model(self)
        dict['cookies'] = parse_sub_model(self.cookies.all())
        if 'thirdPartyCookies' in dict:
            dict['thirdPartyCookies'] = parse_sub_model(self.thirdPartyCookies.all())
        if 'onAccept' in dict:
            dict['onAccept'] = self.onAccept.get_dict(enable=True)
        if 'onRevoke' in dict:
            dict['onRevoke'] = self.onRevoke.get_dict(enable=False)
        return dict

    class Meta:
        verbose_name = "Optional Cookie Control"
        verbose_name_plural = "Optional Cookie Controls"


class TextValue(TranslatableModel):
    translations = TranslatedFields(
        title=models.TextField(null=True, blank=True),
        # This site uses cookies to store information on your computer.
        #
        intro=models.TextField(null=True, blank=True),
        # Some of these cookies are essential, while others help us to improve your experience by providing insights into how the site is being used.
        #
        acceptSettings=models.TextField(null=True, blank=True),
        # 	I Accept
        #
        acceptRecommended=models.TextField(null=True, blank=True),
        # Accept Recommended Settings
        #
        accept=models.TextField(null=True, blank=True),
        # Accept
        #
        rejectSettings=models.TextField(null=True, blank=True),
        # I Do Not Accept
        #
        reject=models.TextField(null=True, blank=True),
        # I Do Not Accept
        #
        settings=models.TextField(null=True, blank=True),
        # Cookie Preferences
        #
        necessaryTitle=models.TextField(null=True, blank=True),
        # Necessary Cookies
        #
        necessaryDescription=models.TextField(null=True, blank=True),
        # Necessary cookies enable core functionality such as page navigation and access to secure areas. The website cannot function properly without these cookies, and can only be disabled by changing your browser preferences.
        #
        thirdPartyTitle=models.TextField(null=True, blank=True),
        # Some cookies require your attention
        #
        thirdPartyDescription=models.TextField(null=True, blank=True),
        # Consent for the following cookies could not be automatically revoked. Please follow the link(s) below to opt out manually.
        #
        on=models.TextField(null=True, blank=True),
        # On
        #
        off=models.TextField(null=True, blank=True),
        # Off
        #
        notifyTitle=models.TextField(null=True, blank=True),
        # Your choice regarding cookies on this site
        #
        notifyDescription=models.TextField(null=True, blank=True),
        # We use cookies to optimise site functionality and give you the best possible experience.
        #
        closeLabel=models.TextField(null=True, blank=True),
        # Close
        #
        cornerButton=models.TextField(null=True, blank=True),
        # (used by screen readers) Set cookie preferences.
        #
        landmark=models.TextField(null=True, blank=True),
        # (used by screen readers) Cookie preferences.
        #
    )

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        # language = get_current_language()
        # return self.known_translation_getter('title', default=None, language_code=language, any_language=True)[0]
        return self.title

    def get_dict(self):
        dict = parse_model(self)
        return dict


# Pro versions only

class Branding(models.Model):
    name = models.CharField(help_text=_('A Unique identifier for this branding'), max_length=255)

    fontFamily = models.CharField(help_text=_("CSS font-family for the entire module e.g. Arial, sans-serif"),
                                  max_length=255, null=True, blank=True)
    # The CSS font-family that you'd like to use for the entire module.
    #
    # string default: Arial, sans-serif
    #
    fontSizeTitle = models.CharField(help_text=_("CSS font-size for the main (h2) title e.g. 1.2em"), max_length=255,
                                     null=True, blank=True)
    # The CSS font-size that you'd like to use for the main (h2) title when the module is opened.
    #
    # string 1.2em
    #
    fontSizeHeaders = models.CharField(help_text=_("CSS font-size for the sub (h3) titles e.g. 1em"), max_length=255,
                                       null=True, blank=True)
    # The CSS font-size that you'd like to use for the sub (h3) titles when the module is opened.
    #
    # string 1em
    #
    fontSize = models.CharField(help_text=_("CSS font-size throughout the module e.g. 0.8em"), max_length=255,
                                null=True, blank=True)
    # The CSS font-size that you'd like to use throughout the module for body text.
    #
    # string 0.8em
    #
    fontColor = ColorField(help_text=_("CSS color for all text and icons within the module."), blank=True, null=True)
    # The CSS color that you'd like to use for all text and icons within the module.
    #
    # string dark theme default: #FFF light theme default: #333
    #
    backgroundColor = ColorField(help_text=_("CSS background-color within the module."), blank=True, null=True)
    # The CSS background-color that you'd like to use throughout the module.
    #
    # string dark theme default: #313147 light theme default: #f4f4f4
    #
    acceptText = ColorField(help_text=_("CSS color for text of the module's primary 'accept' buttons"), blank=True,
                            null=True)
    # The CSS color that you'd like to use for the text within the module's primary 'accept' buttons.
    #
    # string dark theme default: #fff; light theme default: #111125
    #
    acceptBackground = ColorField(help_text=_("CSS background-color for the module's primary 'accept' buttons"),
                                  blank=True, null=True)
    # The CSS background-color that you'd like to use for the module's primary 'accept' buttons.
    #
    # string dark theme default: #313147; light theme default: #fff
    #
    rejectText = ColorField(
        help_text=_("The CSS color that you'd like to use for the text within the module's primary 'reject' buttons."),
        blank=True, null=True)
    # The CSS color that you'd like to use for the text within the module's primary 'accept' buttons.
    #
    # string dark theme default: #fff; light theme default: #111125
    #
    rejectBackground = ColorField(
        help_text=_("The CSS background-color that you'd like to use for the module's primary 'reject' buttons."),
        blank=True, null=True)
    # The CSS background-color that you'd like to use for the module's primary 'accept' buttons.
    #
    # string dark theme default: #313147; light theme default: #fff
    #
    toggleText = ColorField(help_text=_("CSS color for the toggle button's text"), blank=True, null=True)
    # The CSS color that you'd like to apply to the toggle button's text.
    #
    # string dark theme default: #FFF light theme default: #333
    #
    toggleColor = ColorField(help_text=_("CSS background-color for the movable part of the toggle slider"), blank=True,
                             null=True)
    # The CSS background-color that you'd like to use for the movable part of the toggle slider.
    #
    # string dark theme default: #2f2f5f light theme default: #000
    #
    toggleBackground = ColorField(help_text=_("CSS background-color for the toggle background."), blank=True, null=True)
    # The CSS background-color that you'd like to use for the toggle background.
    #
    # string dark theme default: #111125 light theme default: #555
    #
    alertText = ColorField(help_text=_("CSS color within the alert areas"), blank=True, null=True)
    # The CSS color that you'd like to use within the alert areas, such as to announce manual user actions for third party cookies.
    #
    # string dark theme default: #fff; light theme default: #000
    #
    alertBackground = ColorField(help_text=_("CSS background-color to highlight the alert areas"), blank=True,
                                 null=True)
    # The CSS background-color that you'd like to use to highlight the alert areas, such as to announce manual user actions for third party cookies.
    #
    # string dark theme default: #111125 light theme default: #eaeaea
    #
    buttonIcon = FilerImageField(help_text=_('Icon in the bottom corner'), blank=True, null=True,
                                 on_delete=models.SET_NULL)
    # The URL address of an image you'd like to use instead of the CIVIC C icon in the bottom corner.
    #
    # string
    #
    buttonIconWidth = models.CharField(help_text=_("If buttonIcon exists, the css width"), max_length=255, null=True,
                                       blank=True)
    # If buttonIcon exists, the css width that you'd like this image to be sized to.
    #
    # string default: 64px
    #
    buttonIconHeight = models.CharField(help_text=_("If buttonIcon exists, the css height"), max_length=255, null=True,
                                        blank=True)
    # If buttonIcon exists, the css height that you'd like this image to be sized to.
    #
    # string default: 64px
    #
    removeIcon = models.NullBooleanField(help_text=_(
        "Whether or not to remove the button icon entirely. Please note, if you do this, you will need to present an alternative trigger to run the module's open() function."),
                                         null=True, blank=True)
    # Whether or not to remove the button icon entirely. Please note, if you do this, you will need to present an alternative trigger to run the module's open() function.
    #
    # boolean default: false
    #
    removeAbout = models.NullBooleanField(help_text=_("Whether or not to remove the 'About this tool' link"), null=True,
                                          blank=True)

    # Whether or not to remove the 'About this tool' link to CIVIC at the bottom of the module.
    #
    # boolean default: false

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def get_dict(self):
        dict = parse_model(self)
        if 'buttonIcon' in dict:
            dict['buttonIcon'] = self.buttonIcon.url
        return dict


# TODO
class Accessibility(models.Model):
    accessKey = models.CharField(help_text=_('Remaps the accesskey that the module is assigned to'), max_length=512,
                                 null=True, blank=True)

    highlightFocus = models.NullBooleanField(
        help_text=_('Determines if the module should use more accentuated styling to highlight elements in focus'),
        null=True, blank=True)

    overlay = models.NullBooleanField(null=True, blank=True,
                                      help_text=_(
                                          "Determines if the module should use an overlay to accentuate the presence of an open notification bar or panel and discourage use of the main site while these elements are open."))

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.accessKey or self.highlightFocus

    def get_dict(self):
        dict = parse_model(self)
        return dict


class iabConfig(models.Model):
    description = models.CharField(help_text=_('Description of iabCMP'), max_length=512,
                                   default='Selected companies may access and use certain information on your device to serve relevant advertisements')

    globalVendorListLocation = models.CharField(help_text=_('Remaps the accesskey that the module is assigned to'),
                                                max_length=512,
                                                default='https://vendorlist.consensu.org/vendorlist.json')

    language = models.CharField(
        help_text=_('Two letter ISO language code that should be used to display information about IAB purposes.'),
        max_length=128, default='en')

    gdprAppliesGlobally = models.BooleanField(
        help_text=_('Determines whether or not consent should be obtained from all users regardless of their location'),
        default=True)

    recommendedState = models.BooleanField(help_text=_(
        'Determines whether or not the 5 IAB purposes should be accepted as part of your recommended settings.'),
                                           default=True)

    def get_recommendedState(self):
        if self.recommendedState:
            return {1: True, 2: True, 3: True, 4: True, 5: True}

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return "iabCMP: {iabcmp}".format(iabcmp=self.description[:30])

    def get_dict(self):
        dict = parse_model(self)
        return dict


class iabText(TranslatableModel):
    translations = TranslatedFields(
        panelTitle=models.TextField(null=True, blank=True),
        panelIntro1=models.TextField(null=True, blank=True),
        panelIntro2=models.TextField(null=True, blank=True),
        panelIntro3=models.TextField(null=True, blank=True),
        aboutIab=models.TextField(null=True, blank=True),
        iabName=models.TextField(null=True, blank=True),
        iabLink=models.TextField(null=True, blank=True),
        dataUse=models.TextField(null=True, blank=True),
        vendors=models.TextField(null=True, blank=True),
        purposes=models.TextField(null=True, blank=True),
        specialPurposes=models.TextField(null=True, blank=True),
        features=models.TextField(null=True, blank=True),
        specialFeatures=models.TextField(null=True, blank=True),
        purposeLegitimateInterest=models.TextField(null=True, blank=True),
        vendorLegitimateInterest=models.TextField(null=True, blank=True),
        relyConsent=models.TextField(null=True, blank=True),
        relyLegitimateInterest=models.TextField(null=True, blank=True),
        acceptAll=models.TextField(null=True, blank=True),
        rejectAll=models.TextField(null=True, blank=True),
        savePreferences=models.TextField(null=True, blank=True),
    )

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        # language = get_current_language()
        # return self.known_translation_getter('title', default=None, language_code=language, any_language=True)[0]
        return self.label

    def get_dict(self):
        dict = parse_model(self)
        return dict


class CCPAConfig(TranslatableModel):
    translations = TranslatedFields(

        # The text that you wish to call your terms by, for example Privacy Statement.
        name=models.CharField(max_length=255),

        # The text description that introduces your privacy statement.
        # string
        description=models.TextField(help_text=_('Text introducing the privacy statement'), null=True, blank=True),

    )
    # The URL where your terms may be accessed. This link will try to open in a new tab, so it may point to a PDF document without closing the user's access to your site.
    url = models.CharField(help_text=_('URL where your terms may be accessed'), max_length=512, null=True, blank=True)

    # The date that your privacy statement was last issued, in the format of dd/mm/yyyy.
    updated = models.DateField(help_text=_('Terms updated date'), null=True, blank=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def get_dict(self):
        dict = parse_model(self)
        dict['updated'] = self.updated.strftime('%d/%m/%Y')
        return dict


class CookieControl(models.Model):

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_enabled = models.BooleanField(default=True)

    # Controlling Cookies
    # ------------------------------
    # https://www.civicuk.com/cookie-control/documentation#controlling-cookies

    apiKey = models.CharField(max_length=255)
    product = models.CharField(max_length=255, choices=COOKIE_CONTROL_PRODUCT_CHOICES)

    # Cookies
    # ------------------------------
    # This is a list of cookies names necessary for your website's core functionality, that you wish to protect from the module's deleteAll() function.
    # Note - it is possible to use the * wildcard at the end of a cookie name, if you want all cookies that start with this prefix to be protected.
    # array of strings
    necessaryCookies = models.ManyToManyField(Cookie,
                                              help_text=_(
                                                  "List of cookie names necessary for your website's core functionality,"),
                                              blank=True)

    # This is a list of purposes that your website may use.
    # array of objects
    optionalCookies = models.ManyToManyField(PurposeObject,
                                             help_text=_("List of Optional Cookie Groups that your website may use."),
                                             blank=True)

    # Main Settings
    # ------------------------------
    # Determines how many days the consent of the user will be remembered for.
    consentCookieExpiry = models.PositiveIntegerField(default=90, blank=True, null=True,
                                                      help_text=_(
                                                          "Determines how many days the consent of the user will be remembered for."))
    # Cookie Control will respect user given consent until either the cookie expires, or there is a change in your privacy statement.
    # object
    statement = models.ForeignKey(Statement,
                                  help_text=_(
                                      "Cookie Control will respect user given consent until either the cookie expires, or there is a change in your privacy statement."),
                                  on_delete=models.CASCADE, null=True, blank=True)

    # Determines whether or not Cookie Control should record the user's granting or revoking of consent.
    logConsent = models.NullBooleanField(
        help_text=_("Determines how many days the consent of the user will be remembered for."))

    encodeCookie = models.NullBooleanField(help_text=_(
        "If the value of Cookie Control's own cookie should be encoded as a Uniform Resource Identifier (URI)"))

    subDomains = models.NullBooleanField(help_text=_(
        "Determines whether Cookie Control's own cookie is saved to the top level domain, and therefore accessible on all sub domains, or disabled and saved only to the request host."))

    # IABCMP and CCPA configuration and Text
    # ------------------------------
    # The mode in which Cookie Control runs, either 'GDPR' or 'CCPA'
    mode = models.CharField(max_length=10, choices=COOKIE_CONTROL_MODE_CHOICES, default='GDPR',
                            help_text=_("The mode in which Cookie Control runs, either 'GDPR' or 'CCPA'"))

    # The country code of the country that determines legislation of reference.
    publisherCC = models.CharField(help_text=_("Country code of the country that determines legislation of reference."),
                                   null=True, blank=True, default='GB', max_length=10)

    # Determines whether or not Cookie Control runs as and the IAB TCF v2.0 compliant CMP.
    iabCMP = models.BooleanField(
        help_text=_('Determines whether or not Cookie Control runs as and the IAB TCF v2.0 compliant CMP. '
                    'Please note that when using Cookie Control as an IAB CMP, you cannot use any of the more subtle interfaces like notify or box. IAB requires certain view and text so Cookie Control will render in open state.'),
        default=False)

    iabConfig = models.ForeignKey(iabConfig,
                                  help_text=_(
                                      "Cookie Control offers support for the IAB Transparency and Consent Framework (TCF v1.1), should the property iabCMP be enabled."),
                                  on_delete=models.CASCADE, null=True, blank=True)

    iabText = models.ForeignKey(iabText,
                                help_text=_(
                                    "You may also configure the text used to introduce the IAB category / panels"),
                                on_delete=models.CASCADE, null=True, blank=True)

    # When using Cookie Control in CCPA mode, use this object to customise the CCPA required link name and description.
    ccpaConfig = models.ForeignKey(CCPAConfig,
                                   help_text=_(
                                       "When in CCPA mode, use this to customise the CCPA required link name and description"),
                                   on_delete=models.CASCADE, null=True, blank=True)

    # Appearance and behaviour
    # https://www.civicuk.com/cookie-control/documentation#customising
    # ------------------------------
    # Determines the initial display state of Cookie Control.
    initialState = models.CharField(max_length=255, choices=COOKIE_CONTROL_INITIAL_STATE_CHOICES, null=True, blank=True,
                                    help_text=_(
                                        "Possible values are either open, closed, notify (pro licenses only), top (pro licenses only) or box (pro licenses only)."))

    # Determines whether the module only shows its initialState once, or if it continues to replay on subsequent page loads
    notifyOnce = models.NullBooleanField(null=True, blank=True,
                                         help_text=_(
                                             "Determines whether the module only shows its initialState once, or if it continues to replay on subsequent page loads until the user has directly interacted with it "))

    # shows a reject button alongside the accept button on the notification bar
    rejectButton = models.NullBooleanField(null=True, blank=True,
                                           help_text=_(
                                               "shows a reject button alongside the accept button on the notification bar, or alongside the 'accept recommended settings' button when the panel is open"))

    # Determines the display type and behaviour of Cookie Control.
    layout = models.CharField(max_length=255, choices=COOKIE_CONTROL_LAYOUT_CHOICES, null=True, blank=True,
                              help_text=_("[Pro version only] Display type and behaviour of Cookie Control"))

    # Determines the side of the display Cookie Control will occupy.
    position = models.CharField(max_length=255, choices=COOKIE_CONTROL_POSITION_CHOICES, null=True, blank=True,
                                help_text=_("Determines the side of the display Cookie Control will occupy."))

    # Determines the appearance of Cookie Control.
    theme = models.CharField(max_length=255, choices=COOKIE_CONTROL_THEME_CHOICES, null=True, blank=True,
                             help_text=_("Determines the appearance of Cookie Control"))

    # Determines the control toggle for each item within optionalCookies
    toggleType = models.CharField(max_length=255, choices=COOKIE_CONTROL_TOGGLE_TYPE_CHOICES, null=True, blank=True,
                                  help_text=_("Determines the control toggle for each item within optionalCookies"))

    # This property is used to control what will happen when the user clicks on either of the 'Accept' or 'Accept recommended settings' buttons.
    acceptBehaviour = models.CharField(max_length=255, choices=COOKIE_CONTROL_ACCEPT_CHOICES, null=True, blank=True,
                                       help_text=_(
                                           "This property is used to control what will happen when the user clicks on either of the 'Accept' or 'Accept recommended settings' buttons. "))

    # If set to false the Cookie Control main window will remain open when the user clicks on either of the accept or reject buttons
    closeOnGlobalChange = models.NullBooleanField(null=True, blank=True,
                                                  help_text=_(
                                                      "If set to false the Cookie Control main window will remain open when the user clicks on either of the accept or reject buttons, and the user will have to explicitly close it using the X close icon at the top right, or the close button."))

    # Determines the closing behaviour of the module.
    closeStyle = models.CharField(max_length=255, choices=COOKIE_CONTROL_CLOSE_STYLE_CHOICES, null=True, blank=True,
                                  help_text=_("Determines the closing behaviour of the module."))

    # Set this to false if you are using the notify interface and don't wish to show the (X) close icon on it.
    notifyDismissButton = models.NullBooleanField(null=True, blank=True,
                                                  help_text=_(
                                                      "Set this to false if you are using the notify interface and don't wish to show the (X) close icon on it."))

    # Determines the appearance of the settings button on the notification bar.
    settingsStyle = models.CharField(max_length=50, choices=COOKIE_CONTROL_SETTINGS_STYLE_CHOICES, null=True,
                                     blank=True,
                                     help_text=_(
                                         "Determines the appearance of the settings button on the notification bar."))

    # Determines the text used by Cookie Control.
    text = models.ForeignKey(TextValue,
                             help_text=_("Determines the text used by Cookie Control."),
                             on_delete=models.CASCADE, null=True, blank=True)

    # By default, only plain text is accepted within Text Object properties. If this property is set to true, HTML content will also be accepted.
    # setInnerHTML
    # Ignored as we don't store html strings

    # locale - Ignored for now
    # With pro and pro_multisite licenses, you are able to set all aspects of the module's styling,
    # and remove any back links to CIVIC.
    branding = models.ForeignKey(Branding,
                                 help_text=_(
                                     "[Pro version only] Set all aspects of the module's styling, and remove any back links to CIVIC."),
                                 on_delete=models.SET_NULL, null=True, blank=True)

    # Either add the value all, or a list of 2 letter ISO codes for the countries you wish to disable the module for.
    excludedCountries = CountryField(multiple=True, blank=True,
                                     help_text=_(
                                         "[Pro version only] able the module entirely for visitors outside of the EU. Either add the value all, or a list of 2 letter ISO codes for the countries you wish to disable the module"))

    # Defines a function to be triggered after the module initiates the defined configuration.
    onLoad = models.ForeignKey(CallbackFunction,
                               help_text=_("Defines a function to be triggered after the module initiates."),
                               on_delete=models.SET_NULL, null=True, blank=True)

    # If set to true the CookieControl cookie will be marked with the SameSite:Strict flag. Otherwise it will be flagged with SameSite:None, which however will mean that in some browsers Cookie Control will not work unless your site is served over HTTPS.
    sameSiteCookie = models.NullBooleanField(null=True, blank=True,
                                             help_text=_(
                                                 "Set to true the SameSite:Strict flag. Otherwise it will be flagged with SameSite:None"))

    #
    # Used in conjuction with the sameSiteCookie property, it controls the value of the SameSite flag for the CookieControl cookie. It can be one of "Strict", "Lax" or "None"
    sameSiteValue = models.CharField(max_length=50, choices=COOKIE_CONTROL_SAME_SITE_CHOICES, null=True, blank=True,
                                     help_text=_(
                                         'Used in conjuction with the sameSiteCookie property, it controls the value of the SameSite flag for the CookieControl cookie. It can be one of "Strict", "Lax" or "None"'))

    # Accessibility
    # ------------------------------
    # Determines the accessibility helpers available, such as the accesskey and keyboard focus style.
    accessibility = models.ForeignKey(Accessibility,
                                      help_text=_("Determines the accessibility helpers available."),
                                      on_delete=models.CASCADE, null=True, blank=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def get_necessary_cookies(self):
        nec_cookies = [c.get_dict() for c in self.necessaryCookies.all()]
        nec_cookies = list(set().union(nec_cookies, COOKIE_CONTROL_REQUIRED))
        return nec_cookies

    def get_dict(self):
        dict = parse_model(self)

        dict['necessaryCookies'] = self.get_necessary_cookies()
        dict['optionalCookies'] = parse_sub_model(self.optionalCookies.all())

        if 'statement' in dict:
            dict['statement'] = self.statement.get_dict()
        if 'text' in dict:
            dict['text'] = self.text.get_dict()
        if 'onLoad' in dict:
            dict['onLoad'] = self.onLoad.get_dict()
        if 'accessibility' in dict:
            dict['accessibility'] = self.accessibility.get_dict()
        if 'excludedCountries' in dict:
            dict['excludedCountries'] = [str(c) for c in self.excludedCountries]
        if 'branding' in dict:
            dict['branding'] = self.branding.get_dict()
        if self.iabCMP:
            if 'iabConfig' in dict:
                dict['iabConfig'] = self.iabConfig.get_dict()
            if 'iabText' in dict:
                if not 'text' in dict:
                    dict['text'] = {}
                dict['text']['iabCMP'] = self.iabText.get_dict()
                del dict['iabText']
        if self.mode == 'CCPA':
            if 'ccpaConfig' in dict:
                dict['ccpaConfig'] = self.ccpaConfig.get_dict()

                # Pro + Pro Multisite Options
        if self.product in ['COMMUNITY']:
            if 'initialState' in dict:
                del dict['initialState']
            if 'layout' in dict:
                del dict['layout']
            if 'excludedCountries' in dict:
                del dict['excludedCountries']
            if 'branding' in dict:
                del dict['branding']

        return dict

    class Meta:
        verbose_name = "Cookie Control"
        verbose_name_plural = "Cookie Controls"

