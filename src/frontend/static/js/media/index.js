import { initUpload } from "./upload/init_upload.js";
import { initToggleUpload } from "./upload/toggle_upload.js";
import { initDragAndDrop } from "./dragdrop/init_dragdrop.js";
import { initMediaActions } from "./actions/init_media_actions.js";
import { enhanceVideos } from "./actions/enhance_videos.js";

document.addEventListener("DOMContentLoaded", () => {
  enhanceVideos();
  initUpload();
  initToggleUpload(); 
  initDragAndDrop();
  initMediaActions();
});
