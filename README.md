# Sistema de Monitoramento de Trânsito

Aplicação web desenvolvida com Django para registrar e visualizar ocorrências de trânsito em tempo real na cidade de Apodi.

---

## Tecnologias

* Python
* Django
* SQLite
* HTML, CSS, JavaScript

---

## Funcionalidades

* Cadastro e login de usuários
* Registro de ocorrências (acidente, obra, trânsito)
* Visualização em mapa
* Histórico de ocorrências

---

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/clarissagncvs/transito_apodi
```

### 2. Entrar na pasta

```bash
cd transito_apodi
```

### 3. Criar ambiente virtual

```bash
python -m venv venv
```

#### Em computadores do IF

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
python -m venv venv
venv\Scripts\activate
```

### 4. Ativar o ambiente

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

---

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

#### Em computadores do IF

```bash
pip install asgiref==3.11.1 Django==5.2.13 python-dotenv==1.2.2 sqlparse==0.5.5 tzdata==2025.3
```

---

### 6. Rodar migrações

```bash
python manage.py migrate
```

### 7. Iniciar servidor

```bash
python manage.py runserver
```

---

## Organização com Branches

### 1. Criar uma nova branch

Sempre que iniciar uma funcionalidade ou correção:

```bash
git checkout -b nome-da-branch
```

Exemplo:

```bash
git checkout -b feature/login
```

---

### 2. Fazer alterações

```bash
git add .
git commit -m "Descrição da alteração"
```

---

### 3. Atualizar com a branch principal

```bash
git checkout main
git pull
git checkout nome-da-branch
git merge main
```

---

### 4. Enviar para o repositório remoto

```bash
git push origin nome-da-branch
```

---

### 5. Merge (junção das branches)

```bash
git checkout main
git merge nome-da-branch
```

---

### Padrão de nomes de branches

* feature/nome-da-funcionalidade
* fix/nome-do-problema
* hotfix/nome-urgente

---

### Boas práticas

* Não trabalhar diretamente na main
* Criar uma branch para cada tarefa
* Escrever mensagens de commit claras
* Manter as branches atualizadas
* Excluir branches após o merge

---

## Configuração de Variáveis de Ambiente

### Arquivo `.env`

O projeto utiliza um arquivo `.env` para armazenar informações sensíveis, como:

* Chaves secretas
* Configurações de banco de dados
* Credenciais

Esse arquivo não é versionado.

---

### Como configurar

1. Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

No Windows:

```bash
copy .env.example .env
```

2. Edite o arquivo `.env`:

```env
SECRET_KEY=sua_chave_secreta
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

---

### Arquivo `.env.example`

Modelo das variáveis necessárias:

```env
SECRET_KEY=
DEBUG=
DATABASE_URL=
```

---

### Importante

* Não enviar o `.env` para o repositório
* Cada desenvolvedor deve ter seu próprio `.env`
* Manter o `.env.example` atualizado

---

### Boas práticas

* Atualizar o `.env.example` ao adicionar novas variáveis
* Avisar o time sobre mudanças
* Utilizar valores seguros em produção

---

### Bibliotecas recomendadas

* python-decouple
* django-environ

Facilitam o uso de variáveis de ambiente no Django.
