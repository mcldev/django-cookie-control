from django.conf import settings

COOKIE_CONTROL_REQUIRED_DEFAULT = ['csrftoken',
                                   'django_language',
                                   'sessionid',
                                   'django_privacy_mgmt_preferences',
                                   'AWSALB']

# Get these from settings or default to above values.
COOKIE_CONTROL_REQUIRED = getattr(settings, 'COOKIE_CONTROL_REQUIRED_COOKIES', COOKIE_CONTROL_REQUIRED_DEFAULT)

COOKIE_CONTROL_PRODUCT_CHOICES = (('COMMUNITY', 'COMMUNITY'),
                                  ('PRO', 'PRO'),
                                  ('PRO_MULTISITE', 'PRO_MULTISITE'))

COOKIE_CONTROL_LAWFUL_BASIS_CHOICES = (('consent', 'Consent'),
                                       ('legitimate interest', 'Legitimate Interest'))

#  PRO Setting
COOKIE_CONTROL_INITIAL_STATE_CHOICES = [
    ('All Versions', (
        ('open', 'open'),
        ('closed', 'closed'),
    )
     ),
    ('[Pro Version Only]', (
        ('notify', 'notify'),
        ('top', 'top'),
        ('box', 'box')
    )),
]

COOKIE_CONTROL_LAYOUT_CHOICES = (('slideout', 'slideout'),
                                 ('popup', 'popup'))

COOKIE_CONTROL_POSITION_CHOICES = (('left', 'LEFT'),
                                   ('right', 'RIGHT'))

COOKIE_CONTROL_THEME_CHOICES = (('light', 'LIGHT'),
                                ('dark', 'DARK'))

COOKIE_CONTROL_TOGGLE_TYPE_CHOICES = (('slider', 'slider'),
                                      ('checkbox', 'checkbox'))

COOKIE_CONTROL_CLOSE_STYLE_CHOICES = (('icon', 'icon'),
                                      ('labelled', 'labelled'),
                                      ('button', 'button'))

COOKIE_CONTROL_MODE_CHOICES = (('GDPR', 'GDPR'),
                               ('CCPA', 'CCPA'))

COOKIE_CONTROL_SETTINGS_STYLE_CHOICES = (('link', 'link'),
                                         ('button', 'button'))

COOKIE_CONTROL_SAME_SITE_CHOICES = (('Strict', 'Strict'),
                                    ('Lax', 'Lax'),
                                    ('None', 'None'))

COOKIE_CONTROL_ACCEPT_CHOICES = (('all', 'all'),
                                 ('recommended', 'recommended'))

FUNC_START_STR = "**FUNC-START**"
FUNC_END_STR = "**FUNC-END**"
