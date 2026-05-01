# ── 1. imports ────────────────────────────────
from pathlib import Path
from datetime import timedelta
from django.contrib.messages import constants as messages_constants
from dotenv import load_dotenv
import os

# ── 2. ambiente ───────────────────────────────
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = str(os.getenv("SECRET_KEY"))
DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = ["*"]


# ── 3. apps instalados ────────────────────────
INSTALLED_APPS = [
    # django padrão
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # bibliotecas externas
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    # apps do projeto
    "apps.usuarios",
    "apps.vias",
    "apps.ocorrencias",
    "apps.semaforos",
]


# ── 4. middleware (ordem importa) ─────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",      # sempre primeiro
    "corsheaders.middleware.CorsMiddleware",              # antes do CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    'apps.usuarios.middleware.IPLimitMiddleware',
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ── 5. urls e wsgi ────────────────────────────
ROOT_URLCONF = "setup.urls"
WSGI_APPLICATION = "setup.wsgi.application"


# ── 6. templates ──────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ── 7. banco de dados ─────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "transito.db",
    }
}


# ── 8. cache ─────────────────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'fluxo-trafego-cache',
    }
}


# ── 9. autenticação ───────────────────────────
AUTH_USER_MODEL = "usuarios.Usuario"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "/usuarios/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/usuarios/login/"


# ── 10. internacionalização ────────────────────
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Fortaleza"
USE_I18N = True
USE_TZ = True


# ── 11. arquivos estáticos e mídia ────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ── 12. e-mail ────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = f'Trânsito Apodi <{os.getenv("EMAIL_HOST_USER")}>'

# ── 13. django rest framework ─────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# ── 14. JWT ───────────────────────────────────
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":  timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES":      ("Bearer",),
}


# ── 15. cors ──────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True   # apenas em desenvolvimento


# ── 16. mensagens ─────────────────────────────
MESSAGE_TAGS = {
    messages_constants.DEBUG:   "secondary",
    messages_constants.INFO:    "info",
    messages_constants.SUCCESS: "success",
    messages_constants.WARNING: "warning",
    messages_constants.ERROR:   "danger",
}


# ── 17. chave padrão de auto campo ────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
