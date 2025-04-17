// static/js/media/upload/process_upload.js

import {
  showSuccessToast,
  showErrorToast,
  showWarningModal,
  showErrorModal,
} from "../../utils/alerts.js";

export function processUpload(files) {
  const uploadButton = document.getElementById("uploadButton");
  const progressBar = document.getElementById("progressBar");
  const slideshowId = window.slideshowId;

  if (!slideshowId) {
    showErrorToast("ID da pasta não encontrado.");
    return;
  }

  uploadButton.disabled = true;
  uploadButton.classList.add("opacity-50", "cursor-not-allowed");
  uploadButton.textContent = "Enviando...";

  const formData = new FormData();
  Array.from(files).forEach((file) => formData.append("files", file));

  progressBar.classList.remove("hidden");
  progressBar.value = 0;

  const xhr = new XMLHttpRequest();
  xhr.open("POST", `/admin/media/${slideshowId}/upload`, true);

  xhr.upload.onprogress = (event) => {
    if (event.lengthComputable) {
      const percent = Math.round((event.loaded / event.total) * 100);
      progressBar.value = percent;
    }
  };

  xhr.onload = () => {
    progressBar.value = 100;
    progressBar.classList.add("bg-yellow-500");
    uploadButton.textContent = "Processando...";

    try {
      const res = JSON.parse(xhr.responseText);

      const success = res?.success ?? false;
      const message = res?.message || "Erro ao enviar arquivos.";
      const uploaded = res?.data?.success || [];
      const failed = res?.data?.errors || [];

      if (xhr.status === 403) {
        showErrorToast(message || "Você não tem permissão para enviar arquivos.");
      } else if (success && uploaded.length > 0 && failed.length === 0) {
        showSuccessToast(message || "Arquivos enviados com sucesso.");
        setTimeout(() => window.location.reload(), 2000);
      } else if (uploaded.length > 0 && failed.length > 0) {
        showWarningModal(
          "Upload parcial",
          `
            <strong>✅ Enviados:</strong><br>${uploaded.join("<br>")}<br><br>
            <strong>⚠️ Erros:</strong><br>${failed.join("<br>")}
          `,
          () => window.location.reload()
        );
      } else if (failed.length > 0) {
        showErrorModal("Erro no upload", `<strong>⚠️ Erros:</strong><br>${failed.join("<br>")}`);
      } else {
        showErrorToast(message || "Erro inesperado ao enviar arquivos.");
      }
    } catch (err) {
      console.error("[processUpload] Erro ao processar resposta:", err);
      showErrorToast("Falha ao processar resposta do servidor.");
    }

    resetUI();
  };

  xhr.onerror = () => {
    showErrorToast("Verifique sua conexão.");
    resetUI();
  };

  xhr.send(formData);

  function resetUI() {
    uploadButton.disabled = false;
    uploadButton.classList.remove("opacity-50", "cursor-not-allowed");
    uploadButton.textContent = "Enviar Arquivos";
    progressBar.classList.add("hidden");
  }
}
