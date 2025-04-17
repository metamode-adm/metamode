/**
 * render_access_list.js
 * Renderiza a lista de usuários com acesso ao slideshow.
 */

import { showConfirmModal, showSuccessToast, showErrorToast } from "../../utils/alerts.js";
import { sendRequest } from "../../utils/request.js";

/**
 * Renderiza a lista de usuários com acesso à pasta
 * @param {Array} users - Lista de usuários
 * @param {number|string} slideshowId - ID da pasta (slideshow)
 */
export function renderAccessList(users, slideshowId) {
  const container = document.getElementById("slideshow-access-users");
  container.innerHTML = "";

  if (!users || users.length === 0) {
    container.innerHTML = `<p class="text-sm text-gray-500">Nenhum usuário tem acesso a esta pasta.</p>`;
    return;
  }

  users.forEach(user => {
    const card = document.createElement("div");
    card.className = "flex justify-between items-center bg-gray-100 rounded p-2";

    card.innerHTML = `
      <div>
        <p class="text-sm font-medium">${user.name || user.username}</p>
        <p class="text-xs text-gray-600">${user.email}</p>
      </div>
      <button class="text-red-600 text-sm font-semibold hover:underline" data-user-id="${user.id}">
        Remover
      </button>
    `;

    const removeButton = card.querySelector("button");

    removeButton?.addEventListener("click", () => {
      showConfirmModal({
        title: "Remover acesso?",
        text: `Deseja realmente remover o acesso de "${user.name || user.username}"?`,
        confirmText: "Sim, remover",
        cancelText: "Cancelar",
        onConfirm: async () => {
          try {
            await sendRequest(`/admin/media/${slideshowId}/access/remove/${user.id}`, "DELETE");
            showSuccessToast("Acesso removido.");

            const updated = await sendRequest(`/admin/media/${slideshowId}/access`);
            renderAccessList(updated.data.access, slideshowId);
          } catch (err) {
            console.error(err);
            showErrorToast("Erro ao remover acesso.");
          }
        }
      });
    });

    container.appendChild(card);
  });
}
