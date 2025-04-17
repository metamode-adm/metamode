/**
 * Aguarda qualquer interação do usuário e dispara o início do carrossel.
 * A função `onStart` é chamada após a interação inicial.
 */
export function handleInitialInteraction(onStart) {
    const overlay = document.getElementById("interaction-overlay");
    const carousel = document.getElementById("carousel");
  
    let userInteracted = false;
  
    function requestFullscreen() {
      const element = document.documentElement;
      const request =
        carousel.requestFullscreen ||
        carousel.webkitRequestFullscreen ||
        carousel.mozRequestFullScreen ||
        carousel.msRequestFullscreen ||
        element.requestFullscreen ||
        element.webkitRequestFullscreen;
  
      if (request) {
        try {
          request.call(carousel);
        } catch (e) {
          request.call(element);
        }
      }
    }
  
    function activate() {
      if (!userInteracted) {
        userInteracted = true;
        overlay.classList.add("hidden");
        requestFullscreen();
        onStart();
        
        // 🔥 Exibe o gif de fogo
        const fireGif = document.getElementById("fire-gif");
        if (fireGif) fireGif.classList.remove("hidden");
      }
    }
  
    ["click", "touchstart", "pointerdown", "keydown"].forEach(evt =>
      document.addEventListener(evt, activate)
    );
  }
  