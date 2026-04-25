# Sistema de Monitoramento de Trânsito - Trânsito Apodi

Essa aplicação web foi criada em 2026 como uma atividade complementar interdisciplinar do 3º ano do ensino médio integrado com técnico em Informática, apresentado para as disciplinas de Projeto de Desenvolvimento de Software e Programação com Acesso a Banco de Dados. 
---
## Descrição
A proposta dessa aplicação era solucionar um problema de mobilidade urbana regional, sendo inclusa a elaboração de um projeto da ideia proposta pela sala. A problemática escolhida foi o intenso congestionamento em ruas e desorganização no trânsito da cidade de Apodi, sendo indicada para sua resolução a criação de um sistema de trânsito inteligente que serve para ver o estado do trânsito, registrar ocorrências e visualizá-las.
---
## Tecnologias

<div style="display: flex; gap: 8px; flex-wrap: wrap; margin: 10px 0;">
  <!-- HTML -->
  <a href="https://developer.mozilla.org/en-US/docs/Web/HTML" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white" alt="HTML">
  </a>
  
  <!-- CSS -->
  <a href="https://developer.mozilla.org/en-US/docs/Web/CSS" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white" alt="CSS">
  </a>

  <!-- Java Script -->
  <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  </a>
  
  <!-- Python -->
  <a href="https://www.python.org/" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>

  <!-- Django -->
  <a href="https://www.djangoproject.com/" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  </a>

  <!-- SQLite -->
  <a href="https://www.sqlite.org/" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  </a>
  
</div>

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
python manage.py migrate
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
* fix/nome-erro
* docs/documentação

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

