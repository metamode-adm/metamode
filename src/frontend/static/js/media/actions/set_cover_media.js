// static/js/media/actions/set_cover_media.js

import { showSuccessToast, showErrorToast } from "../../utils/alerts.js";

export function definirComoCapa(mediaId) {
  const slideshowId = window.slideshowId;
  if (!slideshowId || !mediaId) return;

  fetch(`/admin/media/${slideshowId}/set-cover/${mediaId}`, {
    method: "POST",
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        showSuccessToast(data.message);
        
      } else {
        showErrorToast(data.message || "Erro ao definir capa.");
      }
    })
    .catch(() => {
      showErrorToast("Erro de rede ao tentar definir a capa.");
    });
}
