// static/js/media/upload/init_upload.js

import { processUpload } from "./process_upload.js";
import { showErrorToast } from "../../utils/alerts.js";

export function initUpload() {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const fileList = document.getElementById("fileList");
  const fileListContainer = document.getElementById("fileListContainer");
  const uploadButton = document.getElementById("uploadButton");

  if (!dropzone || !fileInput || !fileList || !uploadButton) return;

  // Clique no dropzone
  dropzone.addEventListener("click", () => fileInput.click());

  // Drag visual
  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("border-blue-500", "bg-blue-50");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("border-blue-500", "bg-blue-50");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("border-blue-500", "bg-blue-50");
    fileInput.files = e.dataTransfer.files;
    updateFileList();
  });

  fileInput.addEventListener("change", updateFileList);

  uploadButton.addEventListener("click", () => {
    if (fileInput.files.length === 0) {
      return showErrorToast("Nenhum arquivo selecionado!");
    }
    processUpload(fileInput.files);
  });

  function updateFileList() {
    fileList.innerHTML = "";

    if (fileInput.files.length === 0) {
      fileListContainer.style.display = "none";
      return;
    }

    fileListContainer.style.display = "block";

    Array.from(fileInput.files).forEach((file) => {
      const item = document.createElement("div");
      item.className = "flex justify-between items-center p-2 bg-gray-50 rounded border";
      item.innerHTML = `
        <span class="truncate">${file.name}</span>
        <span class="text-sm text-gray-500">${(file.size / (1024 * 1024)).toFixed(2)} MB</span>`;
      fileList.appendChild(item);
    });
  }
}
