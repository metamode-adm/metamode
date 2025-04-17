# Changelog

Todos os registros de mudanças importantes deste projeto serão documentados aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)  
Este projeto segue o versionamento [SemVer](https://semver.org/lang/pt-BR/).

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
