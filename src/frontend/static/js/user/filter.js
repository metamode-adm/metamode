/**
 * filter.js
 * Módulo responsável pelo filtro da lista de usuários por nome, e-mail, ID ou status.
 */

import { getElement } from "../utils/dom.js";

/**
 * Remove acentos e deixa o texto em minúsculo para facilitar a busca.
 */
function normalize(text) {
  return text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

/**
 * Aplica os filtros de texto e status nos cards de usuários.
 */
function applyUserFilter() {
  const searchTerm = normalize(getElement("filtro-texto").value);
  const selectedStatus = getElement("filtro-status").value;
  const userCards = document.querySelectorAll("#user-list > div");

  userCards.forEach((card) => {
    const name = normalize(card.querySelector("h3").innerText);
    const email = normalize(card.querySelector("p.text-gray-600")?.innerText || "");
    const id = card.id.replace("user-", "");
    const status = card.querySelector("span[data-status]").getAttribute("data-status").toLowerCase();
    const role = card.querySelector("span[data-role]").getAttribute("data-role").toLowerCase();

    const matchesText = name.includes(searchTerm) || email.includes(searchTerm) || id.includes(searchTerm);

    let matchesStatus = true;
    switch (selectedStatus) {
      case "comum":
      case "admin":
      case "superadmin":
        matchesStatus = role === selectedStatus;
        break;
      case "ativo":
        matchesStatus = status === "ativo";
        break;
      case "inativo":
        matchesStatus = status === "inativo";
        break;
    }

    if (matchesText && matchesStatus) {
      card.classList.remove("hidden");
    } else {
      card.classList.add("hidden");
    }
  });
}

/**
 * Inicializa os eventos de filtro da página.
 */
export function initUserFilter() {
  const input = getElement("filtro-texto");
  const select = getElement("filtro-status");

  if (!input || !select) return;

  input.addEventListener("input", applyUserFilter);
  select.addEventListener("change", applyUserFilter);
}
