/**
 * Exibe temporariamente o botão de fechar ao detectar movimentação do mouse
 * e define o comportamento do botão de fechar o carrossel.
 */
export function setupCloseButton() {
    const closeButton = document.getElementById("close-carousel");
    let timeout;
  
    if (!closeButton) return;
  
    document.addEventListener("mousemove", () => {
      closeButton.style.opacity = "1";
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        closeButton.style.opacity = "0";
      }, 3000);
    });
  
    closeButton.addEventListener("click", () => {
      fetch("/logout", { method: "POST" })
        .then(() => (window.location.href = "/login"))
        .catch(() => (window.location.href = "/login"));
    });
  }
  