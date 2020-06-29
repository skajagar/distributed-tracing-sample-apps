"""
Django settings for shopping project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import django_opentracing
import jaeger_client


import wavefront_opentracing_sdk.reporting


from wavefront_sdk import WavefrontProxyClient
from wavefront_opentracing_sdk.reporting import WavefrontSpanReporter
from wavefront_sdk.common import ApplicationTags
from wavefront_sdk import WavefrontDirectClient
from wavefront_opentracing_sdk import WavefrontTracer

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fd&l$kulrvo6jta$eob0nvq_#!p-h*0xujo6w1kfu@8nwg!701'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django_opentracing.OpenTracingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shopping.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shopping.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'



application_tags = ApplicationTags(application="sada-automation-ShoppingApp",
                                   service="inventory",
                                   cluster="us-west-2",
                                   shard="secondary",
                                   custom_tags=[("location", "Oregon")])


proxy_client = WavefrontProxyClient(
    host = os.environ.get('PROXY_SERVER'),
    tracing_port=30000,
    distribution_port=2878,
    metrics_port = os.environ.get('PROXY_PORT')
)

proxy_reporter = WavefrontSpanReporter(client=proxy_client)

direct_client = WavefrontDirectClient(
    server=os.environ.get('WAVEFRONT_SERVER'),
    token=os.environ.get('WAVEFRONT_TOKEN')
)
direct_reporter = WavefrontSpanReporter(client=direct_client)

TRACER = WavefrontTracer(reporter=direct_reporter, application_tags=application_tags)


OPENTRACING_TRACE_ALL = False
OPENTRACING_TRACER = django_opentracing.DjangoTracing(TRACER)