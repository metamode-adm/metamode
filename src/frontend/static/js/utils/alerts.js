/**
 * alerts.js
 * Central de alertas e modais usando SweetAlert2
 * Reúne funções reutilizáveis para mensagens de sucesso, erro, alerta e confirmação.
 */

const defaultToastOptions = {
  toast: true,
  position: "top-end",
  showConfirmButton: false,
};

/**
 * Exibe um toast de sucesso no canto superior direito.
 */
export function showSuccessToast(message = "Ação concluída com sucesso.") {
  Swal.fire({
    ...defaultToastOptions,
    icon: "success",
    title: "Sucesso!",
    text: message,
    timer: 3000,
    customClass: {
      popup: "swal2-toast-success",
    },
  });
}

/**
 * Exibe um toast de erro no canto superior direito.
 */
export function showErrorToast(message = "Ocorreu um erro inesperado.") {
  Swal.fire({
    ...defaultToastOptions,
    icon: "error",
    title: "Erro!",
    text: message,
    timer: 4000,
  });
}

/**
 * Exibe um toast de aviso no canto superior direito.
 */
export function showWarningToast(message = "Atenção!") {
  Swal.fire({
    ...defaultToastOptions,
    icon: "warning",
    title: "Aviso!",
    text: message,
    timer: 4000,
    customClass: {
      popup: "swal2-toast-warning",
    },
  });
}

/**
 * Exibe um modal de alerta com conteúdo HTML.
 */
export function showWarningModal(title, html, callback) {
  Swal.fire({
    icon: "warning",
    title,
    html,
    toast: false,
    position: "center",
    showConfirmButton: true,
    confirmButtonText: "OK",
    buttonsStyling: false,
    customClass: {
      confirmButton:
        "bg-yellow-500 text-white hover:bg-yellow-600 px-4 py-2 rounded font-medium",
    },
  }).then(() => {
    if (typeof callback === "function") callback();
  });
}

/**
 * Exibe um modal de erro com conteúdo HTML.
 */
export function showErrorModal(title, html) {
  Swal.fire({
    icon: "error",
    title,
    html,
    toast: false,
    position: "center",
    showConfirmButton: true,
    confirmButtonText: "OK",
    buttonsStyling: false,
    customClass: {
      confirmButton:
        "bg-red-600 text-white hover:bg-red-700 px-4 py-2 rounded font-medium",
    },
  });
}

/**
 * Exibe um modal de confirmação com botões de confirmação e cancelamento.
 */
export function showConfirmModal({
  title = "Tem certeza?",
  text = "Essa ação não pode ser desfeita.",
  confirmText = "Sim",
  cancelText = "Cancelar",
  onConfirm = null,
}) {
  Swal.fire({
    title,
    text,
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: confirmText,
    cancelButtonText: cancelText,
    showCloseButton: true,
    width: "320px",
    padding: "16px",
    buttonsStyling: false,
    customClass: {
      popup: "swal2-popup-minimal",
      confirmButton:
        "swal2-button-confirm bg-red-600 text-white hover:bg-red-700 px-4 py-2 rounded font-semibold",
      cancelButton:
        "swal2-button-cancel bg-gray-200 text-gray-800 hover:bg-gray-300 px-4 py-2 rounded font-medium",
    },
  }).then((result) => {
    if (result.isConfirmed && typeof onConfirm === "function") {
      onConfirm();
    }
  });
}
