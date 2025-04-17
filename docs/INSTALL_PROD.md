# 🔥 Metamode – Guia de Instalação em Produção

Este guia explica como instalar o Metamode em produção com banco de dados, NGINX, HTTPS e segurança adequada.

---

## ☕ Requisitos

- VPS com Ubuntu 22.04+
- Python 3.11+
- Node.js 20+
- MySQL ou MariaDB
- Git
- NGINX + Certbot

---

## ✅ Etapas

### 1. Clone o projeto
```bash
git clone https://github.com/metamode-adm/metamode.git
cd metamode
```

### 2. Ambiente
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

npm install
npm run build:css:once

cp .env.example .env
# Edite .env com os dados reais
```

### 3. Banco de dados
```sql
CREATE DATABASE metamode CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'metamode'@'localhost' IDENTIFIED BY 'metamode123';
GRANT ALL PRIVILEGES ON metamode.* TO 'metamode'@'localhost';
```

### 4. Migrações e Seeds
```bash
alembic upgrade head
PYTHONPATH=. python scripts/seed_roles_and_permissions.py
PYTHONPATH=. python scripts/seed_default_users.py
```

### 5. Serviço systemd (Gunicorn)
```ini
# /etc/systemd/system/metamode.service
[Unit]
Description=Metamode
After=network.target

[Service]
User=metamode
Group=metamode
WorkingDirectory=/opt/metamode
EnvironmentFile=/opt/metamode/.env
ExecStart=/opt/metamode/.venv/bin/gunicorn -k uvicorn.workers.UvicornWorker src.main:app -b 127.0.0.1:8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable metamode
sudo systemctl start metamode
```

### 6. NGINX + HTTPS (SSL)
```bash
sudo apt install nginx certbot python3-certbot-nginx -y
```
```nginx
# /etc/nginx/sites-available/metamode
server {
    listen 80;
    server_name metamode.seudominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /opt/metamode/src/frontend/static/;
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/metamode /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d metamode.seudominio.com --agree-tos -m seu@email.com
```

### 7. Firewall
```bash
sudo apt install ufw -y
sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable
```

---

## 🔹 Variáveis do .env (detalhado)

```ini
DB_USER=metamode
DB_PASSWORD=metamode123
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=metamode

SECRET_KEY=chave_segura
MAX_UPLOAD_SIZE_MB=500
DEFAULT_TIMEZONE=America/Sao_Paulo
ADMIN_SESSION_EXPIRATION=3600
CAROUSEL_MEDIA_DURATION=5

LOG_LEVEL=INFO
UPLOAD_DIR=uploads
LOG_DIR=logs
ENVIRONMENT=production
```

### ❄️ Explicações:
- `ENVIRONMENT=production`: desativa debug, protege o app e carrega handlers de erro customizados
- `LOG_LEVEL=INFO`: evita logs excessivos em produção
- `SECRET_KEY`: usada para criptografia de sessão
- `UPLOAD_DIR`, `LOG_DIR`: pastas criadas automaticamente

---

## ⚖️ Sobre o Backend (app_setup.py)

O app executa uma série de configurações automáticas para produção:

```python
app.mount("/static", StaticFiles(directory="src/frontend/static"))
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR))

app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY, https_only=False, max_age=settings.ADMIN_SESSION_EXPIRATION)
```

### Recomendado para produção:

| Item                   | Valor Correto Produção                         |
|------------------------|-----------------------------------------------|
| `ENVIRONMENT`          | `production`                                  |
| `LOG_LEVEL`            | `INFO` ou `WARNING`                           |
| `https_only`           | `True` (ativa cookies seguros)                |
| `allow_origins`        | Apenas seu domínio, ex: `https://metamode.com`|
| `allowed_hosts`        | `metamode.com`, `localhost`, etc              |

---

## ✅ Finalizado

- Acesse: https://metamode.seudominio.com
- Certificado SSL ativo via Certbot
- Logs em `logs/app.log`
- Sessões com expiração automática e proteção via cookie

---

## 📊 Extras

- Seeds criam permissões e usuários padrão
- Sistema modular e extensível via FastAPI
- Pastas seguras, com logs rotativos

---


## ❤️ Licença

MIT License

