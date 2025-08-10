# 🔥 Metamode – Guia de Instalação para Desenvolvimento

Este guia explica como instalar e rodar o **Metamode** em um ambiente local de desenvolvimento. Ideal para testes, contribuições e validação de funcionalidades.

---

## ⚙️ Requisitos

Certifique-se de ter os seguintes componentes instalados:

- **Python** 3.11+
- **Node.js** 20+
- **Banco de dados:** MySQL/MariaDB **OU** PostgreSQL (local ou remoto)
- **Git**
- **Editor recomendado:** [Visual Studio Code (VS Code)](https://code.visualstudio.com)

### 🗄️ Instalação do Banco de Dados

**Para MySQL/MariaDB (Ubuntu):**
```bash
sudo apt install python3.11 python3.11-venv mariadb-server nodejs npm git
sudo mysql_secure_installation
```

**Para PostgreSQL (Ubuntu):**
```bash
sudo apt install python3.11 python3.11-venv postgresql postgresql-contrib nodejs npm git
sudo -u postgres createdb metamode
```

**Para Windows:**
- MySQL: [Download MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
- PostgreSQL: [Download PostgreSQL](https://www.postgresql.org/download/windows/)

---

## 🐧 Passo a Passo (Linux)

```bash
git clone https://github.com/metamode-adm/metamode.git
cd metamode

# Criação e ativação do ambiente virtual
python3.11 -m venv .venv
source .venv/bin/activate

# Instalação das dependências Python e Node
pip install -r requirements.txt
npm install
npm run build:css:once

# Configuração das variáveis de ambiente
# Escolha o arquivo .env apropriado para seu banco de dados:

# Para MySQL/MariaDB:
cp .env.mysql.example .env

# Para PostgreSQL:
cp .env.postgresql.example .env

# Ou use o arquivo genérico e configure manualmente:
# cp .env.example .env

# ⚠️ IMPORTANTE: Edite o arquivo .env com suas credenciais do banco
```

### 🛠️ Inicializando o banco de dados

```bash
# Aplicando as migrações com Alembic
alembic upgrade head

# Populando permissões e usuários padrão
PYTHONPATH=. python scripts/seed_roles_and_permissions.py
PYTHONPATH=. python scripts/seed_default_users.py
```

> 📌 Estes scripts criam as permissões e um usuário administrador (admin/admin123).

### ▶️ Iniciando o servidor local

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse em: [http://localhost:8000](http://localhost:8000)

---

## 🪟 Passo a Passo (Windows)

Abra o terminal do **PowerShell** ou terminal integrado do **VS Code**:

```powershell
git clone https://github.com/seu-usuario/metamode.git
cd metamode

# Criação e ativação do ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalação das dependências
pip install -r requirements.txt
npm install
npm run build:css:once

# Configuração das variáveis de ambiente
# Escolha o arquivo .env apropriado para seu banco de dados:

# Para MySQL/MariaDB:
copy .env.mysql.example .env

# Para PostgreSQL:
copy .env.postgresql.example .env

# Ou use o arquivo genérico e configure manualmente:
# copy .env.example .env

# ⚠️ IMPORTANTE: Edite o arquivo .env com suas credenciais do banco
```

### 🛠️ Inicializando o banco de dados

```powershell
alembic upgrade head
$env:PYTHONPATH="."
python scripts/seed_roles_and_permissions.py
python scripts/seed_default_users.py
```

### ▶️ Iniciando o servidor local

```powershell
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Abra no navegador: [http://localhost:8000](http://localhost:8000)

---

## 🔐 Configuração do Arquivo `.env`

O Metamode oferece **três arquivos de exemplo** para facilitar a configuração:

- **`.env.example`** - Configuração genérica (PostgreSQL por padrão)
- **`.env.mysql.example`** - Configuração específica para MySQL/MariaDB
- **`.env.postgresql.example`** - Configuração específica para PostgreSQL

### 🗄️ Configuração do Banco de Dados

**Para MySQL/MariaDB:**
```ini
DB_TYPE=mysql
DB_USER="root"
DB_PASSWORD="sua_senha"
DB_HOST="127.0.0.1"
DB_PORT=3306
DB_NAME=metamode
```

**Para PostgreSQL:**
```ini
DB_TYPE=postgresql
DB_USER="postgres"
DB_PASSWORD="sua_senha"
DB_HOST="127.0.0.1"
DB_PORT=5432
DB_NAME=metamode
```

### 🔧 Outras Configurações Importantes

```ini
# Ambiente de execução
ENVIRONMENT=development  # ou 'production'
LOG_LEVEL=DEBUG          # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Segurança
SECRET_KEY=sua_chave_secreta_aqui  # OBRIGATÓRIO alterar!

# Sistema
MAX_UPLOAD_SIZE_MB=500
DEFAULT_TIMEZONE=America/Sao_Paulo
ADMIN_SESSION_EXPIRATION=3600
CAROUSEL_MEDIA_DURATION=5

# Diretórios
UPLOAD_DIR=uploads
LOG_DIR=logs
```

### 📋 Descrição das Variáveis

| Variável                 | Função                                                                 |
|--------------------------|------------------------------------------------------------------------|
| `DB_TYPE`               | Tipo do banco: `mysql` ou `postgresql`                                |
| `DB_USER/PASSWORD/HOST` | Credenciais de conexão com o banco de dados                           |
| `ENVIRONMENT`           | `development` (debug ativo) ou `production`                           |
| `SECRET_KEY`            | Chave para criptografia de sessões (⚠️ **OBRIGATÓRIO** alterar!)       |
| `MAX_UPLOAD_SIZE_MB`    | Tamanho máximo de upload em MB                                        |
| `CAROUSEL_MEDIA_DURATION` | Duração de cada mídia no carrossel (segundos)                       |
| `ADMIN_SESSION_EXPIRATION` | Tempo de expiração da sessão em segundos                           |

> 🔒 **Dica de Segurança:** Gere uma chave secreta forte com:
> ```bash
> python -c "import secrets; print(secrets.token_urlsafe(32))"
> ```

---

## 🔒 Segurança e Middleware (app_setup.py)

O backend configura automaticamente:

- `SessionMiddleware` para login via cookie seguro
- `CORS` com `allow_origins=["*"]` (⚠️ ajustar em produção)
- `TrustedHostMiddleware` (⚠️ ajustar domínio confiável)
- Pastas públicas `/static` (frontend) e `/uploads` (mídias)

### Em ambiente de **produção**, lembre-se de:

- Usar `ENVIRONMENT=production`
- Alterar `https_only=False` para `True`
- Restringir `allowed_hosts` e `allow_origins` ao seu domínio real

---

## 📂 Estrutura de Pastas

```bash
metamode/
├── .env
├── src/
│   └── backend/
│       ├── core/
│       │   └── app_setup.py
│       ├── config.py
│       └── routes/
├── uploads/       # Gerado automaticamente
├── logs/          # Gerado automaticamente com rotação
├── scripts/       # Seeds de dados
└── README.md
```

---

## 🤝 Contribuições

Contribuições são muito bem-vindas!  
Crie um branch com suas mudanças e envie um Pull Request.

---

## 📄 Licença

Este projeto é distribuído sob a licença MIT.

> © 2025 Metamode Open Source

