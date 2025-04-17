/**
 * delete_slideshow.js
 * Lida com a exclusão da pasta (slideshow).
 */

import {
  showSuccessToast,
  showErrorToast,
  showErrorModal,
  showConfirmModal,
} from "../../utils/alerts.js";

/**
 * Inicializa o botão de exclusão da pasta.
 * @param {Function|String} getSlideshowId - Função que retorna o ID da pasta ou valor fixo.
 */
export function handleDeleteSlideshow(getSlideshowId) {
  const deleteBtn = document.getElementById("delete-slideshow");
  const modal = document.getElementById("slideshow-access-modal");

  if (!deleteBtn) return;

  deleteBtn.addEventListener("click", () => {
    const slideshowId = typeof getSlideshowId === "function"
      ? getSlideshowId()
      : getSlideshowId;

    if (!slideshowId) return;

    showConfirmModal({
      title: "Excluir pasta?",
      text: "Tem certeza que deseja excluir esta pasta? Todas as mídias associadas também serão apagadas.",
      confirmText: "Sim, excluir",
      cancelText: "Cancelar",
      onConfirm: async () => {
        try {
          const response = await fetch(`/admin/slideshow/${slideshowId}`, {
            method: "DELETE",
          });
          const result = await response.json();

          if (result.success) {
            showSuccessToast("Pasta excluída com sucesso.");
            modal.classList.add("hidden");
            setTimeout(() => location.reload(), 1000);
          } else {
            showErrorToast(result.message || "Erro ao excluir a pasta.");
          }
        } catch (error) {
          console.error("[delete_slideshow] Erro:", error);
          showErrorModal("Erro inesperado", "Não foi possível excluir a pasta.");
        }
      },
    });
  });
}
