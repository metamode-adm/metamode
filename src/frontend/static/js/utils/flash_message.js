import { showWarningToast } from "./alerts.js"; // ajuste conforme o caminho

// Exibe alerta de flash_message se estiver presente
if (typeof window.flashMessage !== "undefined" && window.flashMessage) {
  showWarningToast(window.flashMessage);
}
