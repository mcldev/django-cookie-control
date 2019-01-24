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
1. Add a new configuration - can used multiple for different sites on multisite.

![alt text](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/add_control.jpg)