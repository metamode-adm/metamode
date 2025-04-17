/**
 * dom.js
 * Utilitários para manipulação de elementos DOM
 */

export function getElement(id) {
    return document.getElementById(id);
  }
  
  export function clearElement(id) {
    const el = getElement(id);
    if (el) el.innerHTML = "";
  }
  
  export function hideElement(id) {
    const el = getElement(id);
    if (el) el.classList.add("hidden");
  }
  
  export function showElement(id) {
    const el = getElement(id);
    if (el) el.classList.remove("hidden");
  }
  
  export function toggleElement(id) {
    const el = getElement(id);
    if (el) el.classList.toggle("hidden");
  }
  
  export function createElementFromHTML(htmlString) {
    const div = document.createElement("div");
    div.innerHTML = htmlString.trim();
    return div.firstChild;
  }
  