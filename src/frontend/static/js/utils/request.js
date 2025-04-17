/**
 * request.js
 * Utilitários para requisições HTTP com tratamento de erros e respostas padronizadas.
 */

import { showErrorToast } from "./alerts.js";

export async function sendRequest(url, method = "GET", data = null) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(url, options);
    const result = await response.json();

    if (!response.ok) {
      let message = result.message || "Erro na requisição.";

      if (response.status === 403) {
        showErrorToast(message || "Você não tem permissão para realizar esta ação.");
        throw new Error("Permissão negada");
      }

      // Mensagens mais detalhadas se forem múltiplos erros
      if (Array.isArray(result.detail)) {
        message = result.detail.map((e) => e.msg).join(" | ");
      }

      throw new Error(message);
    }

    return result;
  } catch (error) {
    console.error("Erro na requisição:", error);
    if (error.message !== "Permissão negada") {
      showErrorToast(error.message || "Erro inesperado.");
    }
    throw error;
  }
}
