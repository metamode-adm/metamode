# Changelog

Todos os registros de mudanças importantes deste projeto serão documentados aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)  
Este projeto segue o versionamento [SemVer](https://semver.org/lang/pt-BR/).

---

## [1.2.0] – 2025-01-20

### Adicionado
- **Suporte completo ao Docker** com containerização da aplicação
- Dockerfile otimizado com multi-stage build para produção
- docker-compose.yml com PostgreSQL e aplicação orquestrados
- Script de inicialização automática do banco de dados (`init_docker.py`)
- Variável `AUTO_INIT_DB` para controle de inicialização automática
- Arquivo `.env.docker.example` com configurações padrão para Docker
- Documentação completa de instalação via Docker (`INSTALL_DOCKER.md`)
- Arquivo `.dockerignore` para otimização da build
- Volumes persistentes para dados do banco e uploads
- Configuração flexível de portas e credenciais via variáveis de ambiente
- Execução automática de migrações Alembic na inicialização
- Aplicação automática de scripts de seed (roles, permissões, usuários padrão)
- Credenciais padrão pré-configuradas para desenvolvimento
- Suporte a customização de credenciais para produção

### Melhorado
- Processo de instalação simplificado para apenas 2 comandos
- Experiência de desenvolvimento mais rápida com containers
- Isolamento completo do ambiente de desenvolvimento
- Documentação expandida com exemplos práticos

---

## [1.1.0] – 2025-01-20

### Adicionado
- Suporte completo a múltiplos bancos de dados (MySQL/MariaDB e PostgreSQL)
- Detecção automática do tipo de banco de dados baseada na variável `DB_TYPE`
- Arquivos de configuração específicos para cada banco: `.env.mysql.example` e `.env.postgresql.example`
- Arquivos de dependências específicos: `requirements-mysql.txt` e `requirements-postgresql.txt`
- Configuração automática de drivers de banco (aiomysql para MySQL, asyncpg para PostgreSQL)
- Documentação atualizada com instruções de instalação para ambos os bancos
- Melhorias no sistema de migrações com suporte a múltiplos bancos

### Alterado
- Arquivo `config.py` agora suporta configuração dinâmica de banco de dados
- Sistema de migrações Alembic atualizado para detectar automaticamente o tipo de banco
- Documentação de instalação expandida com exemplos específicos para cada banco
- Arquivo `requirements.txt` otimizado para dependências comuns

---

## [1.0.1] – 2025-04-17

### Corrigido
- Reforçada a estabilidade da sessão e conexão com o banco de dados
- Adicionado `pool_pre_ping` e `pool_recycle` ao `create_async_engine` (evita falhas por desconexão)
- Padronizado o tratamento de exceções em `get_current_user_with_permissions` e `auth_service`
- Middleware HTML amigável para erros 401 (não logado), 403 (sem permissão) e 500 (erro interno/banco)
- Redirecionamento com `flash_message` ao tentar acessar slideshow inexistente
- Log de erros de banco aprimorado com `OperationalError`
- Removidas funções obsoletas: `verificar_login`, `verificar_super_admin`

---

## [1.0.0] – 2025-04-16

### Adicionado
- Sistema completo de login e gerenciamento de sessão
- Upload e organização de mídias por grupos (slideshows)
- Gerenciamento de usuários com permissões por pasta
- Interface web responsiva (TailwindCSS + Jinja2)
- Visualização em carrossel com ordenação e capa customizada
- Painel de administração com CRUD completo
- API modular (FastAPI) com banco de dados MariaDB
- Logs rotativos e estrutura profissional de diretórios
- Deploy automatizado com systemd + Nginx (modo IP ou domínio)

### Conhecidos
- [BUG] Sessões simultâneas com o mesmo usuário em diferentes dispositivos podem gerar instabilidade momentânea (erro 500). Correção prevista para próxima versão.
