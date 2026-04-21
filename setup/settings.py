# Importa ferramentas para lidar com caminhos e variáveis de ambiente
from pathlib import Path, os

# Importa função para carregar variáveis do arquivo .env
from dotenv import load_dotenv

# Carrega as variáveis do .env (como SECRET_KEY, DEBUG, etc.)
load_dotenv()

# Define o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


# Chave secreta do projeto (vem do .env)
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# DEBUG ativado apenas se estiver como "True" no .env
DEBUG = os.getenv('DEBUG') == 'True'

# Lista de hosts permitidos (vazio em desenvolvimento)
ALLOWED_HOSTS = ["*"]


# Libera requisições de qualquer origem (CORS) — só para desenvolvimento
CORS_ALLOW_ALL_ORIGINS = True


# Apps instalados no projeto
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Bibliotecas externas
    'corsheaders',
    'rest_framework',

    # Seus apps
    'apps.ocorrencias',
    'apps.semaforos',
    'apps.usuarios',
    'apps.vias',
]


# Middlewares (ordem importa!)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Arquivo principal de URLs
ROOT_URLCONF = 'setup.urls'


# Configuração de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Diretório global de templates
        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        # Permite buscar templates dentro dos apps também
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Configuração WSGI
WSGI_APPLICATION = 'setup.wsgi.application'


# Banco de dados (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Define que você está usando um usuário customizado
AUTH_USER_MODEL = 'usuarios.Usuario'


# Validações de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Idioma e fuso horário
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Fortaleza'

USE_I18N = True
USE_TZ = True


# Arquivos estáticos (CSS, JS, imagens)
STATIC_URL = '/static/'

# Diretório onde estão seus arquivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configuração do Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}