# 📌 Mensagens de erro e sucesso centralizadas

# 🔐 Mensagens de Login
LOGIN_REQUIRED = "Você precisa estar logado para acessar esta página."
LOGIN_SUCCESS = "Login realizado com sucesso."
LOGOUT_SUCCESS = "Logout realizado com sucesso."
LOGIN_ERROR_INVALID_CREDENTIALS = "Usuário ou senha inválidos."
LOGIN_ERROR_NO_PERMISSION = "Você não tem permissão de administrador."
NO_ADMIN_PERMISSION = "Você não tem permissão para acessar esta página."
SUPERADMIN_REQUIRED = "Ação permitida apenas para superadministradores."
LOGIN_ERROR_INTERNAL = "Erro interno ao tentar fazer login. Tente novamente mais tarde."

# 👤 Mensagens de Usuário
USER_CREATE_SUCCESS = "Usuário criado com sucesso."
USER_DELETE_SUCCESS = "Usuário removido com sucesso."
USER_NOT_FOUND = "Usuário não encontrado."
USER_UPDATE_SUCCESS = "Usuário atualizado com sucesso."
USER_ALREADY_EXISTS = "Usuário já existe com esse email ou username."
USER_FIELDS_REQUIRED = "Todos os campos obrigatórios devem ser preenchidos."
USER_DELETE_CONFIRM = "O usuário será removido permanentemente!"
USER_PASSWORD_MISMATCH = "As senhas não coincidem!"
USER_SUPERADMIN_REQUIRED = "Ação permitida apenas para superadministradores."
USER_EMAIL_ALREADY_EXISTS = "O e-mail já está em uso."
USER_PASSWORD_WEAK = "A senha deve ter pelo menos 8 caracteres, 1 maiúscula, 1 minúscula, 1 número e 1 caractere especial."
USER_UPDATE_ERROR = "Erro ao atualizar usuário."
USER_CANNOT_DELETE_ADMIN = "Não é permitido excluir um usuário administrador."
USER_CANNOT_EDIT_ADMIN = "Não é permitido editar um usuário administrador."

# 📂 Mensagens de Slideshow
SLIDESHOW_CREATED_SUCCESS = "Slideshow criado com sucesso."
SLIDESHOW_CREATION_FAILED = "Erro ao criar slideshow."
SLIDESHOW_NOT_FOUND = "Slideshow não encontrado."
SLIDESHOW_ALREADY_EXISTS = "Já existe uma pasta com esse identificador."
SLIDESHOW_NAME_DUPLICATE = "Já existe uma pasta com esse identificador."
SLIDESHOW_REQUIRED_FIELDS = "Título e identificador são obrigatórios."
SLIDESHOW_UPDATE_SUCCESS = "Informações da pasta atualizadas com sucesso."
SLIDESHOW_UPDATE_ERROR = "Erro ao atualizar informações da pasta."
SLIDESHOW_DELETE_SUCCESS = "Pasta excluída com sucesso."
SLIDESHOW_DELETE_ERROR = "Erro ao excluir a pasta."

# 🖼️ Mensagens de Mídia
MEDIA_DELETE_SUCCESS = "Mídia removida com sucesso."
MEDIA_NOT_FOUND = "Mídia não encontrada."
MEDIA_ORDER_UPDATE_SUCCESS = "Ordem atualizada com sucesso."
MEDIA_ORDER_UPDATE_ERROR = "Erro ao atualizar ordem das mídias."
MEDIA_UPLOAD_PARTIAL_ERROR = "Alguns arquivos não foram enviados corretamente."
MEDIA_INVALID_IDS = "IDs de mídia inválidos para este slideshow."
MEDIA_SET_COVER_SUCCESS = "Capa atualizada com sucesso."
MEDIA_SET_COVER_ERROR = "Erro ao atualizar a capa."
MEDIA_SHARED_FILE_SKIP = "🔁 Arquivo compartilhado com outras mídias. Apenas removendo do banco."

# 📁 Mensagens de Upload
UPLOAD_SUCCESS = "Arquivos enviados com sucesso!"
UPLOAD_ERROR_INVALID_TYPE = "Arquivo '{filename}' possui tipo inválido."
UPLOAD_ERROR_FORBIDDEN_MEDIA_TYPE = "Tipo de mídia '{media_type}' não é permitido."
UPLOAD_ERROR_FILE_TOO_LARGE = "O arquivo '{filename}' excede o tamanho máximo de {max_size_mb}MB."
UPLOAD_ERROR_GENERIC = "Erro ao enviar arquivos: {error}"

# 👥 Mensagens de Acesso a Slideshows
ACCESS_USER_ADDED_SUCCESS = "Usuário adicionado com sucesso."
ACCESS_USER_ALREADY_EXISTS = "Usuário já tem acesso a esta pasta."
ACCESS_USER_NOT_FOUND = "Usuário não encontrado."
ACCESS_USER_REMOVED_SUCCESS = "Acesso removido com sucesso."
ACCESS_USER_REMOVE_ERROR = "Erro ao remover acesso."
ACCESS_SLIDESHOW_NOT_FOUND = "Pasta não encontrada."
ACCESS_LOAD_SUCCESS = "Dados da pasta carregados com sucesso."
ACCESS_SEARCH_SUCCESS = "Usuários encontrados com sucesso."
ACCESS_SEARCH_ERROR = "Erro ao buscar usuários."
ACCESS_USER_LIST_SUCCESS = "Pastas encontradas"

# 🌎 Mensagens Globais para o Frontend
SUCCESS_OPERATION = "Operação realizada com sucesso!"
ERROR_UNEXPECTED = "Erro inesperado! Tente novamente mais tarde."
ERROR_CONNECTION = "Erro de conexão! Verifique sua conexão com a internet."
INTERNAL_SERVER_ERROR = "Erro interno do servidor. Tente novamente mais tarde."
CONFIRM_YES = "Sim, continuar"
CONFIRM_CANCEL = "Cancelar"

# ⚠️ Mensagens de Validação
INVALID_IDENTIFIER_GENERATED = "O identificador gerado automaticamente não é válido. Escolha um manualmente."

# 🔒 Mensagens para editar perfil
PROFILE_UPDATE_SUCCESS = "Perfil atualizado com sucesso."
PROFILE_UPDATE_ERROR = "Erro ao atualizar o perfil."
PASSWORD_UPDATE_SUCCESS = "Senha atualizada com sucesso."
PASSWORD_UPDATE_ERROR = "Erro ao atualizar a senha."
PASSWORD_WEAK = "A nova senha é muito fraca. Escolha uma senha mais segura."

# 🔑 Mensagens de Permissão
NO_PERMISSION_MSG = "Você não tem permissão para executar esta ação."
