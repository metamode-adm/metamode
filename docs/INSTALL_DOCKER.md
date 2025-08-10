# 🐳 Instalação via Docker

Este guia mostra como instalar o Metamode usando Docker de forma simples e flexível.

---

## 📋 Pré-requisitos

- **Docker** instalado ([Download Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** instalado (geralmente vem com o Docker Desktop)
- **Git** para clonar o repositório

---

## 🚀 Instalação Rápida

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/metamode.git
cd metamode
```

### 2. Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo
cp .env.docker.example .env

# Edite o arquivo .env com suas configurações
# IMPORTANTE: Altere pelo menos o SECRET_KEY!
```

### 3. Inicie os serviços
```bash
docker-compose up -d
```

### 4. Acesse a aplicação
Abra seu navegador em: **http://localhost:8080**

---

## 🗄️ Inicialização do Banco de Dados

O Metamode oferece **inicialização automática** do banco de dados via Docker:

### 🔄 Modo Automático (Padrão)
```bash
# No arquivo .env
AUTO_INIT_DB=true
```

**O que acontece automaticamente:**
1. ✅ Executa `alembic upgrade head` (migrações)
2. ✅ Executa `scripts/seed_roles_and_permissions.py` (roles e permissões)
3. ✅ Executa `scripts/seed_default_users.py` (usuário admin padrão)

### ⚙️ Modo Manual
```bash
# No arquivo .env
AUTO_INIT_DB=false
```

**Para inicialização manual:**
```bash
# Entre no container
docker-compose exec metamode bash

# Execute os comandos manualmente
alembic upgrade head
PYTHONPATH=. python scripts/seed_roles_and_permissions.py
PYTHONPATH=. python scripts/seed_default_users.py
```

> 💡 **Recomendação:** Use `AUTO_INIT_DB=true` para facilidade, ou `false` para controle total.

---

## ⚙️ Configurações Flexíveis

### 🔌 Personalizando a Porta

Edite o arquivo `.env`:
```bash
# Para acessar em uma porta diferente
METAMODE_PORT=9000  # Acesso via http://localhost:9000
```

### 🌐 Integração com Nginx Existente

Se você já tem um Nginx configurado:

1. Configure uma porta interna no `.env`:
```bash
METAMODE_PORT=3001  # Porta interna
```

2. Configure seu Nginx para fazer proxy:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 🔧 Modo Desenvolvimento

Para desenvolvimento com acesso ao banco:
```bash
# No arquivo .env, descomente:
DB_EXTERNAL_PORT=5432
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

Isso permite conectar ao PostgreSQL via `localhost:5432`.

---

## 📁 Estrutura de Dados

O Docker cria volumes persistentes para:
- **uploads_data**: Arquivos enviados pelos usuários
- **logs_data**: Logs da aplicação
- **postgres_data**: Dados do banco PostgreSQL

Seus dados ficam seguros mesmo se você parar/reiniciar os containers.

---

## 🛠️ Comandos Úteis

### Visualizar logs
```bash
# Logs de todos os serviços
docker-compose logs -f

# Logs apenas da aplicação
docker-compose logs -f metamode

# Logs apenas do banco
docker-compose logs -f db
```

### Parar os serviços
```bash
docker-compose down
```

### Reiniciar os serviços
```bash
docker-compose restart
```

### Atualizar a aplicação
```bash
# Parar, reconstruir e iniciar
docker-compose down
docker-compose up -d --build
```

### Backup do banco de dados
```bash
docker-compose exec db pg_dump -U metamode metamode > backup.sql
```

### Restaurar backup
```bash
docker-compose exec -T db psql -U metamode metamode < backup.sql
```

---

## 🔐 Credenciais Padrão do PostgreSQL

### 📋 Credenciais Pré-configuradas

O arquivo `.env.docker.example` já vem com credenciais padrão para facilitar a instalação:

```bash
# Credenciais padrão do PostgreSQL
DB_USER=metamode
DB_PASSWORD=metamode123
DB_NAME=metamode
```

### 🔄 Como Funciona

1. **Container PostgreSQL** usa essas variáveis para criar:
   - Usuário: `metamode`
   - Senha: `metamode123`
   - Database: `metamode`

2. **Aplicação MetaMode** conecta automaticamente usando as mesmas credenciais

3. **Sincronização automática** entre banco e aplicação via variáveis de ambiente

### 🛡️ Para Produção

**IMPORTANTE**: Altere as credenciais em produção!

```bash
# Exemplo de credenciais seguras
DB_USER=meu_usuario_prod
DB_PASSWORD=MinhaSenh@SuperSegur@123!
DB_NAME=metamode_prod
```

---

## 🔒 Configurações de Segurança

### Variáveis Importantes no `.env`:

```bash
# OBRIGATÓRIO: Altere para uma chave segura!
SECRET_KEY=sua-chave-super-secreta-aqui

# Credenciais do banco (altere em produção)
DB_USER=metamode
DB_PASSWORD=metamode123
DB_NAME=metamode

# Limite de upload (em MB)
MAX_UPLOAD_SIZE_MB=100

# Timezone
TIMEZONE=America/Sao_Paulo
```

---

## 🚨 Solução de Problemas

### Porta já em uso
```bash
# Erro: "port is already allocated"
# Solução: Altere METAMODE_PORT no .env
METAMODE_PORT=8081
```

### Problemas de permissão
```bash
# Se houver problemas de permissão com volumes
sudo chown -R $USER:$USER uploads logs
```

### Container não inicia
```bash
# Verifique os logs para identificar o problema
docker-compose logs metamode
```

### Resetar completamente
```bash
# CUIDADO: Isso apaga todos os dados!
docker-compose down -v
docker-compose up -d --build
```

---

## 🌟 Vantagens do Docker

- ✅ **Instalação simples**: Apenas 3 comandos
- ✅ **Isolamento**: Não interfere com outras aplicações
- ✅ **Portabilidade**: Funciona igual em qualquer sistema
- ✅ **Flexibilidade**: Fácil personalização de portas
- ✅ **Backup simples**: Dados em volumes nomeados
- ✅ **Atualizações fáceis**: Rebuild automático

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs: `docker-compose logs -f`
2. Consulte a [documentação oficial do Docker](https://docs.docker.com/)
3. Abra uma issue no repositório do projeto