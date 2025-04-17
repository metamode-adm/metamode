/**
 * form.js
 * Responsável pela criação, edição e validação de usuários com base em roles.
 */

import { showSuccessToast, showErrorToast, showWarningToast } from "../utils/alerts.js";
import { sendRequest } from "../utils/request.js";
import { getElement } from "../utils/dom.js";

const BASE_URL = "/admin/usuarios";

/**
 * Exibe notificação e recarrega a página se sucesso.
 */
function exibirNotificacao(success, message) {
  if (success) {
    showSuccessToast(message);
    setTimeout(() => location.reload(), 1500);
  } else {
    showErrorToast(message);
  }
}

/**
 * Validação da senha.
 */
function validarSenha(password) {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;
  return regex.test(password);
}

/**
 * Criação de novo usuário.
 */
export async function criarUsuario() {
  const username = getElement("username").value.trim();
  const email = getElement("email").value.trim();
  const password = getElement("password").value.trim();
  const isActive = getElement("is_active").checked;
  const role = getElement("role").value;

  if (!username || !email || !password) {
    return showErrorToast("Todos os campos devem ser preenchidos!");
  }

  if (!validarSenha(password)) {
    return showWarningToast(
      "A senha deve ter pelo menos 8 caracteres, 1 maiúscula, 1 minúscula, 1 número e 1 caractere especial (!@#$%^&*)"
    );
  }

  const userData = {
    username,
    email,
    password,
    is_active: isActive,
    role,
  };

  try {
    const result = await sendRequest(BASE_URL, "POST", userData);
    exibirNotificacao(result.success, result.message);
  } catch (error) {
    // Erro já tratado em sendRequest
  }
}

/**
 * Abre o modal de edição com os dados preenchidos.
 */
export function abrirModalEdicao({ id, username, email, isActive, role }) {
  const modal = getElement("edit-modal");
  if (!modal) return showErrorToast("❌ Modal de edição não encontrado.");

  getElement("edit-user-id").value = id;
  getElement("edit-username").value = username;
  getElement("edit-email").value = email;
  getElement("edit-password").value = "";
  getElement("edit-confirm-password").value = "";
  getElement("edit-is-active").checked = isActive === "true";

  const roleSelect = getElement("edit-role");
  if (roleSelect) {
    roleSelect.value = role || "comum";
  }

  modal.classList.remove("hidden");
}

/**
 * Salva as alterações feitas no modal de edição.
 */
export async function salvarEdicao() {
  const userId = getElement("edit-user-id").value;
  const username = getElement("edit-username").value.trim();
  const email = getElement("edit-email").value.trim();
  const password = getElement("edit-password").value.trim();
  const confirmPassword = getElement("edit-confirm-password").value.trim();
  const isActive = getElement("edit-is-active").checked;
  const role = getElement("edit-role").value;

  if (!username || !email) {
    return showWarningToast("Os campos de Nome e E-mail são obrigatórios!");
  }

  if (password && password !== confirmPassword) {
    return showWarningToast("As senhas não coincidem!");
  }

  if (password && !validarSenha(password)) {
    return showWarningToast(
      "A senha deve ter pelo menos 8 caracteres, 1 maiúscula, 1 minúscula, 1 número e 1 caractere especial (!@#$%^&*)"
    );
  }

  const userData = {
    username,
    email,
    is_active: isActive,
    role,
  };

  if (password) {
    userData.password = password;
  }

  try {
    const result = await sendRequest(`${BASE_URL}/${userId}`, "PUT", userData);
    exibirNotificacao(result.success, result.message);
  } catch (error) {
    // Erro tratado por sendRequest
  }
}
