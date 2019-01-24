# django-cookie-control
A Django plugin to integrate the Civic UK Cookie Control (https://www.civicuk.com/cookie-control)

The plugin is compatible with Django, DjangoCMS and Django/CMS multisite.

## To install
Install the application via pip:

`pip install django-cookie-control`

Add 'django_cookie_control' to installed apps:

`INSTALLED_APPS = [
...
'django_cookie_control',
...]`

## To configure

For a full list of configuration settings see the Civic UK site, here:

https://www.civicuk.com/cookie-control/v8/documentation

Plugin configuration overview:

1. Add a new configuration - can used multiple for different sites on multisite.

![Add New](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/add_control.jpg)

2. Configure Main Settings
 - Site name
 - API key
 - Cookie Control product version: Community, Pro, Pro Multisite

![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/main_settings.jpg)

3. Display Options
- Position
- Theme style
- Toggle type
- Close style

![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/display_settings.jpg)

4. Text and Accessibility

![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/configure_accessibility.jpg)

5. Custom Settings

![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/custom_settings.jpg)

6. Pro and Pro_Multisite Settings
A series of settings for the paid Pro plugins, including:
- Custom text
- Custom formatting

![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/pro_settings_only.jpg)

7. Cookies
- Necessary Cookies
    - A simple list of cookie names, including wildcards that are necessary for the site
    - A default list for Django, DjangoCMS, and AWS are already included.
- Optional Cookies
    - Add an optional cookie or package of cookies that can be turned off for the site
    - Using separate functions On Accept or for On Revoke the cookies can be customised to be disable or enabled.

![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/optional_cookie_control.jpg)


