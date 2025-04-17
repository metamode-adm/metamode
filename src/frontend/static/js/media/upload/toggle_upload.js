export function initToggleUpload() {
    const toggleBtn = document.getElementById("toggle-upload");
    const section = document.getElementById("upload-section");
  
    if (!toggleBtn || !section) return;
  
    toggleBtn.addEventListener("click", () => {
      section.classList.toggle("hidden");
      toggleBtn.textContent = section.classList.contains("hidden")
        ? "Exibir área de upload"
        : "Ocultar área de upload";
    });
  }
  