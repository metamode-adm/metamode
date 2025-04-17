// static/js/media/dragdrop/reorder_service.js

import { showSuccessToast, showErrorToast } from "../../utils/alerts.js";

export function sendReorderRequest() {
  const mediaCards = document.querySelectorAll(".draggable-media");
  const slideshowId = window.slideshowId;

  if (!slideshowId || mediaCards.length === 0) return;

  const newOrder = Array.from(mediaCards).map((el) => parseInt(el.dataset.id));

  fetch(`/admin/media/${slideshowId}/reorder`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newOrder),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        showSuccessToast(data.message || "Ordem atualizada com sucesso!");
      } else {
        showErrorToast(data.message || "Erro ao atualizar ordem.");
    
        // Se foi erro de permissão, desfazendo visualmente a reordenação (recarga)
        if (data.message?.includes("perm") || data.message?.includes("Permissão")) {
          setTimeout(() => window.location.reload(), 500);
        }
      }
    })
    .catch(() => {
      showErrorToast("Falha na conexão ao reordenar.");
    });
}
