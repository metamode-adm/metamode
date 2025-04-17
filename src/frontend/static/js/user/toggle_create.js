/**
 * toggle_create.js
 * Lida com o botão de ocultar/exibir o formulário de criação de usuário.
 */

import { getElement } from "../utils/dom.js";

document.addEventListener("DOMContentLoaded", () => {
  const section = getElement("create-user-section");
  const toggleBtn = getElement("toggle-create-user");

  if (!toggleBtn || !section) return;

  toggleBtn.addEventListener("click", () => {
    section.classList.toggle("hidden");
    toggleBtn.textContent = section.classList.contains("hidden")
      ? "Criar novo usuário"
      : "Fechar criação de usuário";
  });

  // Define o texto inicial
  toggleBtn.textContent = "Criar novo usuário";
});
