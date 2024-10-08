from pathlib import Path
import os 
import django
from django.utils.encoding import force_str
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r8&=%bkyoroxzqd+rml6h&rmspq-h@!(k29%(%8cq)rw7a@ll)'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('db_type')=="SERVER":
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'employee',
    'authapp',
    'product',
]

if os.environ.get("db_type") == "SERVER":
    INSTALLED_APPS.append('storages')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'employee.middleware.RequestPathMiddleware'
]

ROOT_URLCONF = 'oqc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
        # 'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'employee.context_processors.header_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'oqc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
SERVER_PSQL = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'qms-database',
    'USER': 'protrack',
    'PASSWORD': os.environ.get("pg_pass"),
    'HOST': 'qms-database.cx2su2waigj7.ap-south-1.rds.amazonaws.com',
    'PORT': '5432',
}

LOCAL_PSQL = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'QMS',
    'USER': 'QMS_Admin',
    'PASSWORD': os.environ.get("local_psql_pass"),
    'HOST': 'localhost',
    'PORT': '5432',
}

DB = {"SERVER": SERVER_PSQL, "LOCAL": LOCAL_PSQL}

DATABASES = {
    'default': DB[os.environ.get("db_type")]
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# OTP Email
# temporarily using gmail account
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'qmsindkal@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get("email_pass")

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'authapp/static')]
STATIC_URL = '/static/'
if os.environ.get("db_type") == "SERVER":
    AWS_STORAGE_BUCKET_NAME = 'qms-server-bucket'
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.environ.get("access_key_id")
    AWS_SECRET_ACCESS_KEY = os.environ.get("secret_access_key")
    AWS_S3_REGION_NAME = 'ap-south-1'
    MEDIA_ROOT = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# WKHTMLTOPDF_PATH = 'C:\Program Files\wkhtmltopdf'

SILENCED_SYSTEM_CHECKS = ['2_0.W001', 'ckeditor.W001']

CKEDITOR_UPLOAD_PATH = 'content/ckeditor/'

django.utils.encoding.force_text = force_str

CKEDITOR_CONFIGS = {
    'default': {
        'allowedContent': True,
        'width': '500px',
        'skin': 'moono-lisa',
        'removeDialogTabs': 'image:Link;image:advanced',
        'toolbar': [
            {'items': ['Table', 'Image',]},
        ],
        'filebrowserUploadUrl': '/ckeditor_image_upload/',
        'filebrowserBrowseUrl': '/server_media_browse/',
        'filebrowserImageBrowseUrl': '/server_media_browse/?type=Images',
    },
    'full': {
        'allowedContent': True,
        'width': '650px',
        'skin': 'moono-lisa',
        'removeDialogTabs': 'image:Link;image:advanced',
        'toolbar': [
            {'items': ['Table', 'Image',]},
        ],
        'filebrowserUploadUrl': '/ckeditor_image_upload/',
        'filebrowserImageBrowseUrl': '/server_media_browse/?type=Images',
        'filebrowserBrowseUrl': '/server_media_browse/'
    }
}
