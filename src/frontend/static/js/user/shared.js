/**
 * shared.js
 * Exibe e gerencia as pastas (slideshows) compartilhadas com um usuário.
 */

import { getElement, createElementFromHTML } from "../utils/dom.js";
import { showConfirmModal, showSuccessToast, showErrorToast } from "../utils/alerts.js";
import { sendRequest } from "../utils/request.js";

/**
 * Remove o acesso de um usuário a uma pasta compartilhada.
 */
async function removerAcesso(slideshowId, userId, username, pastaTitle, containerDiv) {
  showConfirmModal({
    title: "Remover acesso?",
    text: `Deseja realmente remover o acesso de ${username} à pasta "${pastaTitle}"?`,
    confirmText: "Sim, remover",
    cancelText: "Cancelar",
    onConfirm: async () => {
      try {
        const result = await sendRequest(`/admin/media/${slideshowId}/access/remove/${userId}`, "DELETE");
        if (result.success) {
          containerDiv.remove();
          showSuccessToast("Acesso removido com sucesso!");
        } else {
          showErrorToast(result.message || "Erro ao remover acesso.");
        }
      } catch (err) {
        showErrorToast("Erro ao remover acesso.");
      }
    },
  });
}

/**
 * Cria o card de exibição de uma pasta compartilhada.
 */
function criarCardPasta(pasta, userId, username) {
  const div = createElementFromHTML(`
    <div class="bg-gray-100 p-4 rounded-lg flex justify-between items-center">
      <div>
        <p class="font-medium text-gray-800">${pasta.title}</p>
        <p class="text-sm text-gray-600">${pasta.description || "Sem descrição"}</p>
      </div>
      <button class="text-red-500 hover:text-red-700 text-sm remove-btn" data-slideshow-id="${pasta.id}">Remover</button>
    </div>
  `);

  div.querySelector(".remove-btn").addEventListener("click", () => {
    removerAcesso(pasta.id, userId, username, pasta.title, div);
  });

  return div;
}

/**
 * Abre o modal com as pastas compartilhadas de um usuário.
 */
async function abrirPastasCompartilhadas(userId, username) {
  const modal = getElement("shared-folders-modal");
  const nameSpan = getElement("shared-user-name");
  const list = getElement("shared-folder-list");

  nameSpan.textContent = username;
  list.innerHTML = "";

  try {
    const result = await sendRequest(`/admin/users/${userId}/slideshows`);
    if (result.success && result.data.length > 0) {
      result.data.forEach((pasta) => {
        const card = criarCardPasta(pasta, userId, username);
        list.appendChild(card);
      });
    } else {
      list.innerHTML = `<p class="text-sm text-gray-500">Nenhuma pasta compartilhada com este usuário.</p>`;
    }

    modal.classList.remove("hidden");
  } catch (error) {
    console.error("Erro ao carregar pastas:", error);
    list.innerHTML = `<p class="text-sm text-red-500">Erro ao carregar as pastas compartilhadas.</p>`;
  }
}

/**
 * Inicializa os eventos dos botões "Ver pastas compartilhadas".
 */
export function initSharedFoldersModal() {
  const btns = document.querySelectorAll(".pasta-btn");
  btns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const userId = btn.dataset.userId;
      const username = btn.dataset.username;
      abrirPastasCompartilhadas(userId, username);
    });
  });

  document.querySelectorAll(".close-shared-modal").forEach((btn) => {
    btn.addEventListener("click", () => {
      getElement("shared-folders-modal").classList.add("hidden");
    });
  });
}
