// static/js/media/dragdrop/init_dragdrop.js

import { sendReorderRequest } from "./reorder_service.js";

export function initDragAndDrop() {
  const grid = document.getElementById("mediaGrid");
  if (!grid) return;

  let draggedItem = null;

  grid.addEventListener("dragstart", (e) => {
    if (e.target.classList.contains("draggable-media")) {
      draggedItem = e.target;
      e.dataTransfer.effectAllowed = "move";
      draggedItem.classList.add("opacity-50");
    }
  });

  grid.addEventListener("dragover", (e) => {
    e.preventDefault();
    const target = e.target.closest(".draggable-media");
    if (target && target !== draggedItem) {
      const rect = target.getBoundingClientRect();
      const isBelowHalf = (e.clientY - rect.top) / rect.height > 0.5;
      grid.insertBefore(draggedItem, isBelowHalf ? target.nextSibling : target);
    }
  });

  grid.addEventListener("dragend", () => {
    if (draggedItem) {
      draggedItem.classList.remove("opacity-50");
      draggedItem = null;
      sendReorderRequest();
    }
  });
}
