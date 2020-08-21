# django-cookie-control

A Django plugin to integrate the Civic UK Cookie Control (https://www.civicuk.com/cookie-control)

The plugin is compatible with Django, DjangoCMS and Django/CMS multisite.

## Updates
- 2020-08-21 Version 4.x + Updated to use Cookie Control version 9.x

## To install
Install the application via pip:

`pip install django-cookie-control`

Add 'django_cookie_control' to installed apps:

`INSTALLED_APPS = [
...
'django_cookie_control',
...]`

Add/Edit the following to `settings.py` if required with required cookies:
```
# DEFAULT if missing:
COOKIE_CONTROL_REQUIRED_COOKIES = ['csrftoken','django_language','sessionid','django_privacy_mgmt_preferences','AWSALB']
```

Run or make migrations:

`python.exe manage.py migrate`

## To configure

For a full list of configuration settings see the Civic UK site, here:

https://www.civicuk.com/cookie-control/documentation

Plugin configuration overview:

1. Add a new configuration:
    
    ![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/add_control.jpg)

2. Configure Main Settings:
    - Site name
    - API key
    - Cookie Control product version: Community, Pro, Pro Multisite
    
    ![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/main_settings.jpg)

3. Settings:

    https://www.civicuk.com/cookie-control/documentation#configuration-options
    - consentCookieExpiry
    - statement
    - logConsent
    - encodeCookie
    - subDomains
    
    ![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/custom_settings.jpg)

4. IAB/CCPA Frameworks:
    
    https://www.civicuk.com/cookie-control/documentation#iab
    - mode
    - publisherCC
    - iabCMP
    - iabConfig
    - iabText
    - ccpaConfig
    
    ![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/iab_ccpa_config.jpg)

5. Appearance and Behaviour:

    https://www.civicuk.com/cookie-control/documentation#customising
    - All other settings
    
    ![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/accessiblity.jpg)
    
6. Accessibility:

    https://www.civicuk.com/cookie-control/documentation#accessibility-object
    - Determines the accessibility helpers available, such as the accesskey and keyboard focus style. 
    ![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/configure_accessibility.jpg)

7. Cookies:

    https://www.civicuk.com/cookie-control/documentation#purpose-object
    * Necessary Cookies
      * A simple list of cookie names, including wildcards that are necessary for the site
      * A default list for Django, DjangoCMS, and AWS are already included.
    * Optional Cookies
      * Add an optional cookie or package of cookies that can be turned off for the site
      * Using separate functions On Accept or for On Revoke the cookies can be customised to be disable or enabled.

    ![](https://raw.githubusercontent.com/mcldev/django-cookie-control/master/docs/images/optional_cookie_control.jpg)





