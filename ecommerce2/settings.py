import os
from django.utils.timezone import timedelta
from pathlib import Path
from .local_settings import *



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

IS_DEVEL=True



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#3%!^7_=up(5)bs3x^_eaz0mo4woir*-ovje)nquy6w@@t4xg&'




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'import_export',
    'rest_framework_simplejwt',

    'products',
    'users',
    'payments',
    'pymysql',
    'mozilla_django_oidc',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce2.urls'

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

WSGI_APPLICATION = 'ecommerce2.wsgi.application'


# Database
    
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'HOST':DB_HOST,
        'USER':DB_USER,
        'PASSWORD':DB_PASS,
        'PORT':DB_PORT,

    }
}


# Password validation

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




AUTHENTICATION_BACKENDS = (
    'ecommerce2.auth_backends.KeycloakOIDCBackend', 
    'django.contrib.auth.backends.ModelBackend',
)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        
    )
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

# Media Files 
MEDIA_ROOT=os.path.join(BASE_DIR,'media/')
MEDIA_URL='/media/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Keycloak OIDC settings

OIDC_RP_CLIENT_ID = "django-client"
OIDC_RP_CLIENT_SECRET = "ElFewLzifo59ktEKbXNhVeIlDphdsqOb"

OIDC_OP_AUTHORIZATION_ENDPOINT = "http://localhost:8080/realms/Ecommerce-Realm/protocol/openid-connect/auth"

OIDC_OP_TOKEN_ENDPOINT = "http://localhost:8080/realms/Ecommerce-Realm/protocol/openid-connect/token"

OIDC_OP_USER_ENDPOINT = "http://localhost:8080/realms/Ecommerce-Realm/protocol/openid-connect/userinfo"

OIDC_OP_JWKS_ENDPOINT = "http://localhost:8080/realms/Ecommerce-Realm/protocol/openid-connect/certs"

OIDC_RP_SIGN_ALGO = "RS256"


LOGIN_REDIRECT_URL = "/api/products/"
LOGOUT_REDIRECT_URL ="/api/products/" 





