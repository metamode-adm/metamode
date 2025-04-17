// static/js/media/actions/remove_media.js

import { showConfirmModal, showSuccessToast, showErrorToast } from "../../utils/alerts.js";

export function removerMidia(mediaId) {
  showConfirmModal({
    title: "Remover mídia?",
    text: "Essa ação não pode ser desfeita.",
    confirmText: "Remover",
    cancelText: "Cancelar",
    onConfirm: async () => {
      const video = document.querySelector(`#media-card-${mediaId} video`);
      if (video) {
        video.pause();
        video.src = "";
        video.load();
      }

      try {
        const res = await fetch(`/admin/media/${mediaId}`, { method: "DELETE" });
        const data = await res.json();

        if (data.success) {
          document.getElementById(`media-card-${mediaId}`)?.remove();
          showSuccessToast(data.message);
        } else {
          showErrorToast(data.message);
        }
      } catch (err) {
        console.error(err);
        showErrorToast("Erro inesperado ao remover mídia.");
      }
    },
  });
}
