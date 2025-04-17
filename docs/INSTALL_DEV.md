# 🔥 Metamode – Guia de Instalação para Desenvolvimento

Este guia explica como instalar e rodar o **Metamode** em um ambiente local de desenvolvimento. Ideal para testes, contribuições e validação de funcionalidades.

---

## ⚙️ Requisitos

Certifique-se de ter os seguintes componentes instalados:

- **Python** 3.11+
- **Node.js** 20+
- **MySQL ou MariaDB** (local ou remoto)
- **Git**
- **Editor recomendado:** [Visual Studio Code (VS Code)](https://code.visualstudio.com)

> 💡 No Ubuntu, instale via:
```bash
sudo apt install python3.11 python3.11-venv mariadb-server nodejs npm git
```

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

# Variáveis de ambiente
cp .env.example .env
# ⚠️ Edite o arquivo .env com as credenciais corretas do banco
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

# Variáveis de ambiente
copy .env.example .env
# ⚠️ Edite o arquivo .env com as credenciais corretas do banco
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

## 🔐 Variáveis do `.env`

```ini
ENVIRONMENT=development
LOG_LEVEL=DEBUG
SECRET_KEY=uma_chave_segura
UPLOAD_DIR=uploads
LOG_DIR=logs
ADMIN_SESSION_EXPIRATION=3600
```

### Descrição das principais variáveis

| Variável                 | Função                                                                 |
|--------------------------|------------------------------------------------------------------------|
| `ENVIRONMENT`           | Define o ambiente (`development` ativa o modo debug)                   |
| `LOG_LEVEL`             | Nível de log (`DEBUG`, `INFO`, `WARNING`, `ERROR`)                     |
| `SECRET_KEY`            | Chave para proteger cookies de sessão                                  |
| `UPLOAD_DIR` / `LOG_DIR`| Diretórios criados automaticamente, usados para uploads e logs         |
| `ADMIN_SESSION_EXPIRATION` | Tempo em segundos antes da sessão expirar                             |

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

