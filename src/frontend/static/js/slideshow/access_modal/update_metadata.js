/**
 * update_metadata.js
 * Atualiza o título e a descrição da pasta (slideshow).
 */

import {
  showSuccessToast,
  showErrorToast,
  showErrorModal,
  showWarningToast,
} from "../../utils/alerts.js";

/**
 * Inicializa o botão de salvar edição de metadados de uma pasta.
 * @param {Function|String} getSlideshowId - Função que retorna o ID da pasta ou valor fixo.
 */
export function handleSaveMetadata(getSlideshowId) {
  const saveBtn = document.getElementById("save-slideshow-access");
  const modal = document.getElementById("slideshow-access-modal");
  const titleInput = document.getElementById("slideshow-access-title");
  const descriptionInput = document.getElementById("slideshow-access-description");

  if (!saveBtn) return;

  saveBtn.addEventListener("click", async () => {
    const title = titleInput.value.trim();
    const description = descriptionInput.value.trim();
    const slideshowId = typeof getSlideshowId === "function" ? getSlideshowId() : getSlideshowId;

    if (!title) {
      return showWarningToast("O título da pasta não pode estar vazio.");
    }

    try {
      const response = await fetch(`/admin/media/${slideshowId}/update`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, description }),
      });

      const result = await response.json();

      if (result.success) {
        showSuccessToast("Pasta atualizada com sucesso!");
        modal.classList.add("hidden");
        setTimeout(() => location.reload(), 1000);
      } else {
        showErrorToast(result.message || "Erro ao atualizar a pasta.");
      }
    } catch (error) {
      showErrorModal("Erro inesperado", "Não foi possível salvar as alterações.");
      console.error("[update_metadata] Falha ao atualizar metadata:", error);
    }
  });
}
