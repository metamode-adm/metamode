// 📁 static/js/carousel/index.js

import { preloadAllMedia } from "./actions/preload.js";
import { handleInitialInteraction } from "./actions/interaction.js";
import { setupCloseButton } from "./actions/close_button.js";
import { startCarousel } from "./actions/carousel_engine.js";

// Inicializa o carrossel após o DOM estar carregado
document.addEventListener("DOMContentLoaded", () => {
  preloadAllMedia();
  handleInitialInteraction(startCarousel);
  setupCloseButton();
});