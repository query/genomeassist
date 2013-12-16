import os


### Useful global definitions.
#
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


### Settings expected to be overridden by local installations.
#
# Default to production mode.
DEBUG = TEMPLATE_DEBUG = False

# Various secrets and security-related settings.
DATABASES = {}
SECRET_KEY = ''
ALLOWED_HOSTS = tuple()

# Bower component installation path.
BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'bower_components')

# Celery broker.
BROKER_URL = ''

# GenomeAssist-specific settings.
ALIGNER_BASE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'aligners')
# Look for aligner binaries in the following directory.
SCHEDULER_BIN_DIR = os.path.join(ALIGNER_BASE_DIR, 'bin')
# Place uploaded reads in the following directory.
SCHEDULER_READ_DIR = os.path.join(ALIGNER_BASE_DIR, 'reads')
# Look for reference sequences in the following directory.
SCHEDULER_REFERENCE_DIR = os.path.join(ALIGNER_BASE_DIR, 'references')


### Settings that should be in effect on every instance.
#
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'djangobower',
    'djcelery',
    'pipeline',
    'south',

    'genomeassist.scheduler',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

WSGI_APPLICATION = 'genomeassist.wsgi.application'
ROOT_URLCONF = 'genomeassist.urls'
LOGIN_REDIRECT_URL = '/'

# Internationalization.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files.
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Needed Bower components.
BOWER_INSTALLED_APPS = (
    'bootstrap#3.0',
    'html5shiv',
    'jquery-timeago',
    'respond',
)

# Celery settings.
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_TRACK_STARTED = True

# Crispy forms settings.
CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_CLASS_CONVERTERS = {
    'select': 'form-control',
    'textarea': 'form-control',
    'textinput': 'form-control',
}

# Pipeline settings.
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'bootstrap/dist/css/bootstrap.css',
            'genomeassist/css/*.css',
        ),
        'output_filename': 'dist/base.css',
        'extra_context': {
            'media': 'screen',
        },
    },
}
PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'jquery/jquery.js',
            'bootstrap/dist/js/bootstrap.js',
            'jquery-timeago/jquery.timeago.js',
            'jquery-deserialize/jquery.deserialize.min.js',
            'genomeassist/js/*.js',
        ),
        'output_filename': 'dist/base.js',
    },
    'ie8': {
        'source_filenames': (
            'html5shiv/dist/html5shiv.js',
            'respond/dest/respond.min.js',
        ),
        'output_filename': 'dist/ie8.js',
    }
}


### Local overrides.
#
execfile(os.path.join(os.path.dirname(__file__), 'local_settings.py'))
