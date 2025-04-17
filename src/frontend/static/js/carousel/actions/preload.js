/**
 * Pré-carrega todas as mídias (imagens e vídeos) e atualiza o overlay de carregamento.
 */
export function preloadAllMedia() {
    const items = document.querySelectorAll(".carousel-item");
    const loadingOverlay = document.getElementById("loading-overlay");
    const loadingText = document.getElementById("loading-text");
    const overlay = document.getElementById("interaction-overlay");
  
    if (items.length === 0) {
      loadingText.textContent = "Nenhuma mídia encontrada.";
      return;
    }
  
    let loadedItems = 0;
  
    const updateProgress = () => {
      loadedItems++;
      const percent = Math.round((loadedItems / items.length) * 100);
      loadingText.textContent = `Carregando mídias... ${percent}%`;
  
      if (loadedItems === items.length) {
        setTimeout(() => {
          loadingOverlay.classList.add("hidden");
          overlay.classList.remove("hidden");
        }, 300);
      }
    };
  
    items.forEach(item => {
      const img = item.querySelector("img");
      const video = item.querySelector("video");
  
      if (img) {
        if (img.complete) updateProgress();
        else {
          img.addEventListener("load", updateProgress);
          img.addEventListener("error", updateProgress);
        }
      } else if (video) {
        video.preload = "auto";
        video.load();
        video.addEventListener("loadeddata", updateProgress);
        video.addEventListener("error", updateProgress);
      }
    });
  }
  