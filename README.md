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

### 3.1 Criar ambiente virtual nos computadores do IF
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
python -m venv venv
venv\Scripts\activate

### 4. Ativar o ambiente
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

### 5. Instalar dependências
pip install -r requirements.txt

### 5.1 instalar dependências nos computadores do IF
pip install asgiref==3.11.1 Django==5.2.13 python-dotenv==1.2.2 sqlparse==0.5.5 tzdata==2025.3

### 6. Rodar migrações
python manage.py migrate

### 7. Iniciar servidor
python manage.py runserver

## Branches
Como trabalhamos com branches
### 1. Criar uma nova branch

Sempre que for iniciar uma nova funcionalidade ou correção:

git checkout -b nome-da-branch

Exemplo:

git checkout -b feature-login
### 2. Fazer alterações

Realize as mudanças normalmente e salve seus commits:

git add .
git commit -m "Descrição da alteração"
### 3. Atualizar a branch principal

Antes de finalizar, garanta que sua branch está atualizada com a main:

git checkout main
git pull
git checkout nome-da-branch
git merge main
### 4. Enviar para o repositório remoto
git push origin nome-da-branch
### 5. Merge (junção das branches)

Após revisão, a branch pode ser integrada à main:

git checkout main
git merge nome-da-branch

Padrão de nomes de branches

Utilizamos um padrão para facilitar a organização:

feature/nome-da-funcionalidade → novas funcionalidades
fix/nome-do-problema → correções de bugs
hotfix/nome-urgente → correções urgentes em produção

### 6. Boas práticas
Nunca trabalhar diretamente na main
Criar uma branch para cada tarefa
Escrever mensagens de commit claras
Manter as branches atualizadas
Excluir branches após o merge
