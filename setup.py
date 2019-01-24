import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_cookie_control',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Django plugin to add and configure the Cookie Control by Civic UK',
    long_description=README,
    url='https://github.com/mcldev/django-cookie-control',
    author='Michael Carder Ltd',
    author_email='codetoolbox@michaelcarder.co.uk',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.11',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django>=1.8',
        'django-parler',
        'django-filer',
        'django-countries',
        'django-colorfield',
    ],
    package_data={
        'readme': ['README.md'],
        'license': ['LICENSE']
    },
)

