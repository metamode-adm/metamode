const menuToggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");
const closeSidebar = document.getElementById("close-sidebar");

if (menuToggle && sidebar && closeSidebar) {
  menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("-translate-x-full");
  });

  closeSidebar.addEventListener("click", () => {
    sidebar.classList.add("-translate-x-full");
  });
}
