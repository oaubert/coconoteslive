# Django settings
import os

# local_settings should define a 'options' dictionary with
# configuration values.
try:
    from local_settings import options
except ImportError:
    options = {}

DEBUG = True
TEMPLATE_DEBUG = DEBUG

APPROOT = os.path.dirname(os.path.dirname(__file__)) + os.sep

ADMINS = (
 (options.get('admin_name', 'Olivier Aubert'), options.get('admin_mail', 'contact@olivieraubert.net')),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': options.get('db_engine', 'django.db.backends.sqlite3'), # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': options.get('db_name', APPROOT + 'db.sqlite3'),  # Or path to database file if using sqlite3.
        'USER': options.get('db_user', ''),                      # Not used with sqlite3.
        'PASSWORD': options.get('db_password', ''),                  # Not used with sqlite3.
        'HOST': options.get('db_host', ''),                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': options.get('db_port', ''),                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(APPROOT, "media/")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = APPROOT + 'static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = options.get('secret_key', 'no_secret_at_all_key')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_requestlogging.middleware.LogSetupMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'server.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'server.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

LOGGING = {
    'version': 1,
    'filters': {
        # Add an unbound RequestFilter.
        'request': {
            '()': 'django_requestlogging.logging_filters.RequestFilter',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(module)s %(levelname)s %(message)s'
        },
        'request_format': {
            'format': '%(remote_addr)s [%(asctime)s] %(username)s "%(request_method)s '
            '%(path_info)s %(server_protocol)s" %(http_user_agent)s '
            '%(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['request'],
            'formatter': 'request_format',
            },
        },
    'loggers': {
        'base': {
            'filters': ['request'],
            },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
            },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
            },
        }
    }

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # Cf http://stackoverflow.com/questions/6957360/admin-login-stopped-functioning-django
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'mla',

    'django.contrib.admin',
    'django_requestlogging',
    'south',
)

if options.get('raven_dsn'):
    RAVEN_CONFIG = {
        'dsn': options.get('raven_dsn', ''),
        }
    INSTALLED_APPS += ( 'raven.contrib.django.raven_compat', )
