# Importa ferramentas para lidar com caminhos e variáveis de ambiente
from pathlib import Path
import os

# Importa função para carregar variáveis do arquivo .env
from dotenv import load_dotenv

# Carrega as variáveis do .env (como SECRET_KEY, DEBUG, etc.)
load_dotenv()

# Define o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


# Chave secreta do projeto (vem do .env)
SECRET_KEY = str(os.getenv("SECRET_KEY"))

# DEBUG ativado apenas se estiver como "True" no .env
DEBUG = os.getenv("DEBUG") == "True"

# Lista de hosts permitidos (liberado em desenvolvimento)
ALLOWED_HOSTS = ["*"]


# Libera requisições de qualquer origem (CORS) — só para desenvolvimento
CORS_ALLOW_ALL_ORIGINS = True


# Apps instalados no projeto
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Bibliotecas externas
    "corsheaders",
    "rest_framework",
    # Seus apps
    "apps.ocorrencias",
    "apps.semaforos",
    "apps.usuarios",
    "apps.vias",
]


# Middlewares (ordem importa!)
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Arquivo principal de URLs
ROOT_URLCONF = "setup.urls"


# Configuração de templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Diretório global de templates
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        # Permite buscar templates dentro dos apps também
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


# Configuração WSGI
WSGI_APPLICATION = "setup.wsgi.application"


# Banco de dados (SQLite)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "transito.db",
    }
}


# Define que você está usando um usuário customizado
AUTH_USER_MODEL = "usuarios.Usuario"


# Validações de senha
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Idioma e fuso horário
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Fortaleza"

USE_I18N = True
USE_TZ = True

# CONFIGURAÇÃO DE ARQUIVOS ESTÁTICOS (CORRIGIDA)

# URL base para acessar arquivos estáticos
STATIC_URL = "/static/"

# Pasta onde você colocou css, js, imagens
STATICFILES_DIRS = [BASE_DIR / "static"]

# Pasta usada pelo Django internamente
STATIC_ROOT = BASE_DIR / "staticfiles"

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' teste

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'clarissavitoria122@gmail.com'  # Seu e-mail real
EMAIL_HOST_PASSWORD = 'rbtp clbn zyex lfiu' # NÃO é a senha normal do e-mail!
DEFAULT_FROM_EMAIL = 'Trânsito Apodi <seu-email@gmail.com>'

# 🔌 DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}
