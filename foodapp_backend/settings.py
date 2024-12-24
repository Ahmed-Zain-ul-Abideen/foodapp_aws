import os
import sys
# from dotenv import load_dotenv
from datetime import timedelta

# load_dotenv()
from pathlib import Path
import mimetypes
from decouple import config
import   firebase_admin
from  firebase_admin  import  credentials
mimetypes.add_type("text/css", ".css", True) 
 
BASE_DIR = Path(__file__).resolve().parent.parent

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__)) 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=mn$5w9f@kn$gtbf20irv(bjve!xraw!rn+avajxo!93h#i#ss'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CSRF_TRUSTED_ORIGINS= ["http://192.168.18.29:8080","http://192.168.18.29:8000","http://192.168.18.67:8080",
    "http://192.168.18.67:8000",      "http://192.168.18.68:8080","http://192.168.18.68:8000",
    "http://192.168.18.51:8080", "http://192.168.18.51:8000",
    
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = ["http://localhost:8080","192.168.18.29","http://192.168.18.29:8080","http://192.168.18.29:8000",
    "http://192.168.18.67:8080","http://192.168.18.67:8000" ,      "http://192.168.18.68:8080","http://192.168.18.68:8000",
    "http://192.168.18.51:8080", "http://192.168.18.51:8000",
]

ALLOWED_HOSTS = ['*','localhost',"192.168.18.29","192.168.18.67","192.168.18.68","192.168.18.51","192.168.18.29",
    "http://192.168.18.29:8080","http://192.168.18.29:8000", "http://192.168.18.67:8080","http://192.168.18.67:8000"  , 
    "http://192.168.18.68:8080","http://192.168.18.68:8000","http://192.168.18.51:8080", "http://192.168.18.51:8000", 
] 

SECURE_CROSS_ORIGIN_OPENER_POLICY = None

sys.dont_write_bytecode = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'crispy_forms',
    'crispy_bootstrap4',
    'social_django',
    'webApp.apps.WebappConfig',
    'rest_framework',
    'fcm_django',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.linkedin_oauth2',  # Add this line for LinkedIn OAuth2
    'channels',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # <--
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'foodapp_backend.urls'

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 
        'DIRS': [
            os.path.join(BASE_DIR, 'lucifer/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages', 
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect', #
            ],
        },
    },
]

WSGI_APPLICATION = 'foodapp_backend.wsgi.application'
ASGI_APPLICATION = 'foodapp_backend.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('localhost', 6379)],
        },
    },
}


CRISPY_TEMPLATE_PACK = 'bootstrap4'

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ahmedzain3305@gmail.com'
EMAIL_HOST_PASSWORD = 'cahmjbrocfgjjngc'


DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = False

#JWT-AUTH
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 1,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
      'rest_framework.permissions.AllowAny',
  ],
   
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  config('DB_Name'),
        'USER':  config('DB_User'),
        'PASSWORD':  config('DB_Password'),
        'HOST':  config('DB_HOST'),
        'PORT':  config('DB_PORT'),  
        'OPTIONS': {  
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8',
        }
    }
}

# AUTHENTICATION_BACKENDS = [
#   'social_core.backends.facebook.FacebookOAuth2'
#   'social_core.backends.linkedin.LinkedinOAuth2',
#   'social_core.backends.instagram.InstagramOAuth2',
#   'django.contrib.auth.backends.ModelBackend',
# ]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    # 'social_core.backends.github.GithubOAuth2', # github <----
    'social_core.backends.twitter.TwitterOAuth', # twitter <----
    # 'social_core.backends.facebook.FacebookOAuth2', # facebook <----
    # 'social_core.backends.google.GoogleOAuth2',  # google <----
    'django.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend",
    # 'social_core.contrib.auth.backends.ModelBackend', 
)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': config('DB_Name'),
#         'USER': config('DB_User'),
#         'PASSWORD': config('DB_Password'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT'),  
#         'OPTIONS': {  
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#             'charset': 'utf8mb4',
#         }
#     }
# }

VAPID_PUBLIC_KEY =  config('VAPID_PUBLIC_KEY')
VAPID_PRIVATE_KEY = config('VAPID_PRIVATE_KEY')
VAPID_EMAIL = config('VAPID_EMAIL')

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

SITE_ID = 1
# REDIRECT_URI = 'http://localhost:8000/lnkd_logi'
ACCOUNT_EMAIL_VERIFICATION = 'none'
# Allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True 


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

font_path = os.path.join(BASE_DIR, 'static/to/serviceAccountKey.json') 
# Path to your service account key file
cred = credentials.Certificate(font_path)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred)

GOOGLE_OAUTH_CLIENT_ID= "787045378804-27otdan5j5ts07bprfgoehi8505inpd4.apps.googleusercontent.com"

# SOCIAL_AUTH_FACEBOOK_KEY =  "438272252233294"  
# SOCIAL_AUTH_FACEBOOK_SECRET = "f9002a288b6516a942243b37f195ff9c" 
SOCIAL_AUTH_FACEBOOK_KEY =  "1913170909106824"  
SOCIAL_AUTH_FACEBOOK_SECRET = "0ecb72a8e2d4a1e580e9f5387e9f3dd5"  


# Linkedin Authentication Setting
SOCIALACCOUNT_PROVIDERS = {
    'linkedin_oauth2': {
        'CLIENT_ID': '774yjmsuovwh04',
        'SECRET': 'UJJwU1s84cVQVXxv',
        'SCOPE': [
            'r_liteprofile',
            'r_emailaddress',
            'w_member_social'
        ],
        'PROFILE_FIELDS': [
            'id',
            'firstName',
            'lastName',
            'profilePicture(displayImage~:playableStreams)',
            'emailAddress'
        ],
    } 
}




# SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '77hb9kwxc4tw5d'
# SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'OOnls1CZ0t8ZwJsV'
# SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['w_member_social', 'openid', 'profile', 'email']
# SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email',
#                                                'formatted-name',
#                                                'public-profile-url',
#                                                'picture-url']
# SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
#     ('id', 'id'),
#     ('formattedName', 'name'),
#     ('emailAddress', 'email_address'),
#     ('pictureUrl', 'picture_url'),
#     ('publicProfileUrl', 'profile_url'),
# ]
# SOCIALACCOUNT_PROVIDERS = {
#     "openid_connect": {
#         "APPS": [
#             {
#                 "provider_id": "linkedin-server",
#                 "name": "LinkedIn OIDC",
# #                 "client_id":  "77hb9kwxc4tw5d",
# #                 "secret":  "OOnls1CZ0t8ZwJsV",
# #                 "settings": {
# #                     "server_url": "https://www.linkedin.com/oauth",
# #                 },
# #             }
# #         ]
# #     },
# }
# SOCIALACCOUNT_PROVIDERS = 
#     {
#         'linkedin':
#            {'SCOPE': ['r_emailaddress'],
#        'PROFILE_FIELDS: ['id',
#                          'first-name',
#                          'last-name',
#                          'email-address',
#                          'picture-url',
#                          'public-profile-url']}
# } 

# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, picture.type(large), link'
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [
    ('name', 'name'),
    ('email', 'email'),
    ('picture', 'picture'),
    ('link', 'profile_url'),
]


LOGIN_URL = 'sign_in'
LOGIN_REDIRECT_URL = 'soc_logi'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'sign_in'

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
