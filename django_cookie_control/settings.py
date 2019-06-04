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
COOKIE_CONTROL_INITIAL_STATE_CHOICES = (('open', 'open'),
                                        ('closed', 'closed'),
                                        ('notify', 'notify'))

COOKIE_CONTROL_LAYOUT_CHOICES = (('slideout', 'slideout'),
                                ('popup', 'popup'))

COOKIE_CONTROL_POSITION_CHOICES = (('LEFT', 'LEFT'),
                                ('RIGHT', 'RIGHT'))

COOKIE_CONTROL_THEME_CHOICES = (('LIGHT', 'LIGHT'),
                                ('DARK', 'DARK'))

COOKIE_CONTROL_TOGGLE_TYPE_CHOICES = (('slider', 'slider'),
                                      ('checkbox', 'checkbox'))

COOKIE_CONTROL_CLOSE_STYLE_CHOICES = (('icon', 'icon'),
                                      ('labelled', 'labelled'),
                                      ('button', 'button'))



FUNC_START_STR = "**FUNC-START**"
FUNC_END_STR = "**FUNC-END**"