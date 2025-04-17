/**
 * index.js
 * Inicialização dos eventos da página de gerenciamento de usuários.
 */

import { criarUsuario, abrirModalEdicao, salvarEdicao } from "./form.js";
import { initUserFilter } from "./filter.js";
import { initSharedFoldersModal } from "./shared.js";
import { showConfirmModal, showSuccessToast, showErrorToast } from "../utils/alerts.js";
import { sendRequest } from "../utils/request.js";
import { getElement } from "../utils/dom.js";

const BASE_URL = "/admin/usuarios";

/**
 * Remove um usuário com confirmação.
 */
function removerUsuario(userId) {
  showConfirmModal({
    title: "Tem certeza?",
    text: "O usuário será removido permanentemente!",
    confirmText: "Sim, remover",
    cancelText: "Cancelar",
    onConfirm: async () => {
      try {
        const result = await sendRequest(`${BASE_URL}/${userId}`, "DELETE");
        showSuccessToast(result.message);
        setTimeout(() => location.reload(), 1000);
      } catch (error) {
        showErrorToast("Erro ao remover usuário.");
      }
    },
  });
}

/**
 * Inicializa os eventos da página após o DOM estar carregado.
 */
document.addEventListener("DOMContentLoaded", () => {
  // Botão: Criar novo usuário
  getElement("criar-usuario")?.addEventListener("click", criarUsuario);

  // Botão: Salvar edição de usuário
  getElement("salvar-edicao")?.addEventListener("click", salvarEdicao);

  // Botões: Fechar modal de edição
  getElement("fechar-modal")?.addEventListener("click", () =>
    getElement("edit-modal").classList.add("hidden")
  );
  getElement("fechar-modal-footer")?.addEventListener("click", () =>
    getElement("edit-modal").classList.add("hidden")
  );

  // Botões: Editar usuários
  document.querySelectorAll(".editar-usuario").forEach((btn) => {
    btn.addEventListener("click", () => {
      abrirModalEdicao({
        id: btn.dataset.id,
        username: btn.dataset.username,
        email: btn.dataset.email,
        isActive: btn.dataset.active,
        role: btn.dataset.role
      });
    });
  });

  // Botões: Remover usuários
  document.querySelectorAll(".remover-usuario").forEach((btn) => {
    btn.addEventListener("click", () => removerUsuario(btn.dataset.id));
  });

  // Botões: Ver pastas compartilhadas
  initSharedFoldersModal();

  // Filtros: Texto e status
  initUserFilter();
});
