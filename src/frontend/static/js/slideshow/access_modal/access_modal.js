/**
 * access_modal.js
 * Controla o modal de permissões e edição de uma pasta (slideshow).
 */

import { loadSlideshowAccess } from "./load_access.js";
import { renderAccessList } from "./render_access_list.js";
import { handleSearchInput } from "./search_users.js";
import { handleDeleteSlideshow } from "./delete_slideshow.js";
import { handleSaveMetadata } from "./update_metadata.js";
import {
  showConfirmModal,
  showErrorToast,
} from "../../utils/alerts.js";

document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("slideshow-access-modal");
  const openButtons = document.querySelectorAll(".open-access-modal");
  const closeModalBtn = document.getElementById("close-slideshow-access-modal");
  const cancelModalBtn = document.getElementById("cancel-slideshow-access");

  let currentSlideshowId = null;

  // Abre o modal e carrega os dados da pasta
  openButtons.forEach(button => {
    button.addEventListener("click", async (e) => {
      e.preventDefault();
      e.stopPropagation();

      currentSlideshowId = button.getAttribute("data-slideshow-id");
      modal.classList.remove("hidden");

      try {
        const data = await loadSlideshowAccess(currentSlideshowId);

        // Preenche os campos de metadados
        document.getElementById("slideshow-access-id").value = data.id || "";
        document.getElementById("slideshow-access-title").value = data.title || "";
        document.getElementById("slideshow-access-description").value = data.description || "";

        // Lista de usuários com acesso
        renderAccessList(data.access, currentSlideshowId);
      } catch (err) {
        showErrorToast(message || "Erro ao carregar dados da pasta.");
      }
    });
  });

  // Fecha o modal
  closeModalBtn?.addEventListener("click", () => modal.classList.add("hidden"));
  cancelModalBtn?.addEventListener("click", () => modal.classList.add("hidden"));

  // Salva as alterações da pasta (passa função para obter ID atual)
  handleSaveMetadata(() => currentSlideshowId);

  // Exclui a pasta
  handleDeleteSlideshow(() => currentSlideshowId);

  // Busca e adiciona usuários
  handleSearchInput(() => currentSlideshowId);
});
