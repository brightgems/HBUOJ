
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import re

from django.utils.translation import gettext_lazy as _
from django_jinja.builtins import DEFAULT_EXTENSIONS
from jinja2 import select_autoescape

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5*9f5q57mqmlz2#f$x1h76&jxy#yortjl1v+l*6hd18$d*yx#0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SITE_ID = 1
SITE_NAME = 'HBUOJ'
SITE_LONG_NAME = 'Hebei University Online Judge'

PYGMENT_THEME = 'pygment-github.css'

# Application definition
INSTALLED_APPS = (
    'judge.apps.SuitConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'judge',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'mptt',
    'reversion',
    'django_social_share',
    'compressor',
    'django_ace',
    'sortedm2m',
    'statici18n',
    'impersonate',
    'django_jinja',
    'import_export',
    'django_gravatar',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'judge.user_log.LogUserAccessMiddleware',
    'judge.timezone.TimezoneMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'judge.middleware.ContestMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

# Impersonate module settings
IMPERSONATE_REQUIRE_SUPERUSER = True
IMPERSONATE_DISABLE_LOGGING = True

SILENCED_SYSTEM_CHECKS = ['urls.W002', 'fields.W342']

ROOT_URLCONF = 'hbuoj.urls'
WSGI_APPLICATION = 'hbuoj.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'match_extension': ('.html', '.txt'),
            'match_regex': '^(?!admin/)',
            'context_processors': [
                # 'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.tz',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'judge.template_context.comet_location',
                'judge.template_context.get_resource',
                'judge.template_context.general_info',
                'judge.template_context.site',
                'judge.template_context.site_name',
                'judge.template_context.misc_config',
                'judge.template_context.math_setting',
            ],
            'autoescape': select_autoescape(['html', 'xml']),
            'trim_blocks': True,
            'lstrip_blocks': True,
            'extensions': DEFAULT_EXTENSIONS + [
                'compressor.contrib.jinja2ext.CompressorExtension',
                'judge.jinja2.DMOJExtension',
                'judge.jinja2.spaceless.SpacelessExtension',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.tz',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGES = [
    ('zh-hans', _('Simplified Chinese')),
    ('en', _('English')),
]


# Your database credentials. Only MySQL is supported by HBUOJ.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hbuoj',
        'USER': 'hbuoj',
        'PASSWORD': 'hbuoj',
        'HOST': '127.0.0.1',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES',
        },
    }
}

ENABLE_FTS = False

# Bridged configuration
BRIDGED_JUDGE_ADDRESS = [('localhost', 9999)]
BRIDGED_DJANGO_ADDRESS = [('localhost', 9998)]
BRIDGED_DJANGO_CONNECT = None

# Event Server configuration
EVENT_DAEMON_USE = False
EVENT_DAEMON_POST = 'ws://localhost:9997/'
EVENT_DAEMON_GET = 'ws://localhost:9996/'
EVENT_DAEMON_POLL = '/channels/'
EVENT_DAEMON_KEY = None

# Internationalization
# Whatever you do, this better be one of the entries in `LANGUAGES`.
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'UTC'
DEFAULT_USER_TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Cookies
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# CDN control.
HIGHLIGHT_BASE_URL = '//cdn.bootcss.com/highlight.js/9.12.0/'
MATHJAX_URL = '//cdn.bootcss.com/mathjax/2.7.4/MathJax.js'
JQUERY_JS = '//cdn.bootcss.com/jquery/2.2.4/jquery.min.js'
SELECT2_JS_URL = '//cdn.bootcss.com/select2/4.0.3/js/select2.min.js'
SELECT2_CSS_URL = '//cdn.bootcss.com/select2/4.0.3/css/select2.min.css'
FONTAWESOME_CSS = '//cdn.bootcss.com/font-awesome/4.7.0/css/font-awesome.min.css'

# Static files (CSS, JavaScript, Images)
DMOJ_RESOURCES = os.path.join(BASE_DIR, 'resources')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'resources'),
]
STATIC_ROOT = '/tmp/static'
STATIC_URL = '/static/'

# django-compressor settings, for speeding up page load times by minifying CSS and JavaScript files.
COMPRESS_OUTPUT_DIR = 'cache'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'
STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)

# Caching. You can use memcached or redis instead.
CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 1024}
        }
    }
}

# Authentication
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
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
ACCOUNT_FORMS = {
    'signup': 'judge.account.forms.MySignupForm',
}
LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

JUDGE_AMQP_PATH = None
DEFAULT_CODE_LANGUAGE = 'CPP14'
