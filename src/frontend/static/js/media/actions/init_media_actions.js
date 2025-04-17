// static/js/media/actions/init_media_actions.js

import { removerMidia } from "./remove_media.js";
import { definirComoCapa } from "./set_cover_media.js";
import { enhanceVideos } from "./enhance_videos.js";

export function initMediaActions() {
    enhanceVideos();

  document.querySelectorAll(".remover-midia").forEach((btn) => {
    btn.addEventListener("click", () => {
      const mediaId = btn.getAttribute("data-id");
      removerMidia(mediaId);
    });
  });

  document.querySelectorAll(".definir-capa").forEach((btn) => {
    btn.addEventListener("click", () => {
      const mediaId = btn.getAttribute("data-id");
      definirComoCapa(mediaId);
    });
  });
}
