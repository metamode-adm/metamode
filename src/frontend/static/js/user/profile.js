/**
 * profile.js
 * Responsável por atualizar o nome, e-mail e senha do próprio usuário.
 */

import { showSuccessToast, showErrorToast, showWarningToast } from "../utils/alerts.js";
import { sendRequest } from "../utils/request.js";
import { getElement } from "../utils/dom.js";

const PROFILE_URL = "/profile/update";
const PASSWORD_URL = "/profile/password";
const LOGOUT_URL = "/logout";

/**
 * Valida se a senha atende aos critérios mínimos.
 */
function validarSenha(password) {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;
  return regex.test(password);
}

/**
 * Força o logout e redireciona o usuário para login.
 */
async function forcarLogout() {
  showSuccessToast("Dados atualizados! Redirecionando para login...");
  setTimeout(() => {
    window.location.href = LOGOUT_URL;
  }, 1800);
}

/**
 * Atualiza nome de usuário e e-mail.
 */
async function atualizarDadosBasicos(username, email) {
  const payload = { username, email };

  try {
    const result = await sendRequest(PROFILE_URL, "PUT", payload);
    if (result.success) {
      showSuccessToast(result.message || "Perfil atualizado com sucesso!");
      return true;
    } else {
      showErrorToast(result.message || "Erro ao atualizar dados.");
      return false;
    }
  } catch {
    showErrorToast("Falha ao atualizar o perfil.");
    return false;
  }
}

/**
 * Atualiza a senha do usuário.
 */
async function atualizarSenha(novaSenha) {
  try {
    const result = await sendRequest(PASSWORD_URL, "PUT", { new_password: novaSenha });
    if (result.success) {
      showSuccessToast(result.message || "Senha atualizada com sucesso!");
      return true;
    } else {
      showErrorToast(result.message || "Erro ao atualizar a senha.");
      return false;
    }
  } catch {
    showErrorToast("Falha ao atualizar a senha.");
    return false;
  }
}

/**
 * Lógica principal do formulário de perfil.
 */
getElement("form-profile-completo").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = getElement("input-username").value.trim();
  const email = getElement("input-email").value.trim();
  const novaSenha = getElement("input-password").value.trim();
  const confirmarSenha = getElement("input-confirm-password").value.trim();

  if (!username || !email) {
    return showWarningToast("Os campos de nome e email são obrigatórios.");
  }

  let alterouDados = await atualizarDadosBasicos(username, email);
  let alterouSenha = false;

  if (novaSenha || confirmarSenha) {
    if (novaSenha !== confirmarSenha) {
      return showWarningToast("As senhas não coincidem.");
    }

    if (!validarSenha(novaSenha)) {
      return showWarningToast(
        "A senha deve ter pelo menos 8 caracteres, 1 maiúscula, 1 minúscula, 1 número e 1 caractere especial (!@#$%^&*)"
      );
    }

    alterouSenha = await atualizarSenha(novaSenha);
  }

  // Limpa os campos de senha
  getElement("input-password").value = "";
  getElement("input-confirm-password").value = "";

  if (alterouDados || alterouSenha) {
    await forcarLogout();
  }
});
