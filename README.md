# Sistema de Monitoramento de Trânsito

Aplicação web desenvolvida com Django para registrar e visualizar ocorrências de trânsito em tempo real na cidade de Apodi

## Tecnologias

- Python
- Django
- SQLite
- HTML, CSS, JavaScript

## Funcionalidades

- Cadastro e login de usuários
- Registro de ocorrências (acidente, obra, trânsito)
- Visualização em mapa
- Histórico de ocorrências

## Como executar o projeto

### 1. Clonar o repositório
git clone https://github.com/clarissagncvs/transito_apodi

### 2. Entrar na pasta
cd transito_apodi

### 3. Criar ambiente virtual
python -m venv venv

### 4. Ativar o ambiente
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

### 5. Instalar dependências
pip install -r requirements.txt

### 6. Rodar migrações
python manage.py migrate

### 7. Iniciar servidor
python manage.py runserver