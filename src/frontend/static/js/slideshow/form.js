/**
 * form.js
 * Controla o modal de criação de uma nova pasta (slideshow).
 * Responsável por validar e enviar o formulário para o backend.
 */

import {
    showSuccessToast,
    showErrorToast,
    showWarningToast
  } from "../utils/alerts.js";
  
  // Espera o DOM estar totalmente carregado
  document.addEventListener("DOMContentLoaded", () => {
    const openBtn = document.getElementById("create-folder-btn");
    const modal = document.getElementById("modal-criar-pasta");
    const closeBtn = document.getElementById("fechar-modal-criar");
    const cancelBtn = document.getElementById("cancelar-criar-pasta");
    const form = document.getElementById("form-criar-pasta");
  
    // Abertura do modal
    openBtn?.addEventListener("click", () => modal.classList.remove("hidden"));
  
    // Fechamento do modal
    closeBtn?.addEventListener("click", () => modal.classList.add("hidden"));
    cancelBtn?.addEventListener("click", () => modal.classList.add("hidden"));
  
    // Submissão do formulário
    form?.addEventListener("submit", async (e) => {
      e.preventDefault();
  
      const title = document.getElementById("slideshow-title").value.trim();
      const description = document.getElementById("slideshow-description").value.trim();
  
      // Validação simples do campo título
      if (!title || title.length < 3) {
        showWarningToast("O título precisa ter pelo menos 3 caracteres.");
        return;
      }
  
      const payload = { title, description };
  
      try {
        const response = await fetch("/admin/media", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
  
        const result = await response.json();
  
        if (response.ok && result.success) {
          showSuccessToast(result.message || "Pasta criada com sucesso.");
          setTimeout(() => window.location.reload(), 1000);
        } else if (response.status === 422) {
          const error = result?.detail?.[0]?.msg || "Erro de validação nos dados.";
          showWarningToast(error);
        } else {
          showErrorToast(result.message || "Erro ao criar a pasta.");
        }
      } catch (err) {
        console.error("Erro ao criar pasta:", err);
        showErrorToast("Erro inesperado. Verifique a conexão.");
      }
    });
  });
  