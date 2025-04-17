/**
 * search_users.js
 * Lida com a busca e adição de usuários ao slideshow.
 */

import { showSuccessToast, showErrorToast } from "../../utils/alerts.js";
import { loadSlideshowAccess } from "./load_access.js";
import { renderAccessList } from "./render_access_list.js";

/**
 * Lida com o input de busca e a adição de usuários ao slideshow.
 * @param {Function|string} getSlideshowId - Função ou string que retorna o ID da pasta.
 */
export function handleSearchInput(getSlideshowId) {
  const input = document.getElementById("slideshow-user-search");
  const resultsContainer = document.getElementById("slideshow-user-results");

  input?.addEventListener("input", async () => {
    const query = input.value.trim();
    const slideshowId = typeof getSlideshowId === "function" ? getSlideshowId() : getSlideshowId;

    if (query.length < 2 || !slideshowId) {
      resultsContainer.innerHTML = "";
      return;
    }

    try {
      const response = await fetch(`/admin/users/search?q=${encodeURIComponent(query)}&slideshow_id=${slideshowId}`);
      const data = await response.json();

      resultsContainer.innerHTML = "";

      if (data.success && data.data.length > 0) {
        data.data.forEach(user => {
          const userCard = document.createElement("div");
          userCard.className = "flex justify-between items-center bg-gray-50 rounded p-2";

          userCard.innerHTML = `
            <div>
              <p class="text-sm font-medium">${user.username}</p>
              <p class="text-xs text-gray-600">${user.email}</p>
            </div>
            <button class="text-blue-600 text-sm font-semibold hover:underline" data-user-id="${user.id}">
              Adicionar
            </button>
          `;

          // Adiciona evento ao botão "Adicionar"
          const addButton = userCard.querySelector("button");
          addButton?.addEventListener("click", async () => {
            try {
              const res = await fetch(`/admin/media/${slideshowId}/access/add`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: user.id }),
              });

              const result = await res.json();

              if (result.success) {
                showSuccessToast("Usuário adicionado.");
                input.value = "";
                resultsContainer.innerHTML = "";

                // Atualiza lista de usuários com acesso
                const updated = await loadSlideshowAccess(slideshowId);
                renderAccessList(updated.access, slideshowId);
              } else {
                showErrorToast(result.message || "Erro ao adicionar usuário.");
              }
            } catch (err) {
              console.error(err);
              showErrorToast("Erro inesperado ao adicionar usuário.");
            }
          });

          resultsContainer.appendChild(userCard);
        });
      } else {
        resultsContainer.innerHTML = `
          <p class="text-sm text-gray-500">Nenhum usuário encontrado.</p>
        `;
      }

    } catch (err) {
      console.error(err);
      showErrorToast("Erro ao buscar usuários.");
    }
  });
}
