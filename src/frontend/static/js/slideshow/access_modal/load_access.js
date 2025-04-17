/**
 * load_access.js
 * Realiza a requisição para buscar os dados da pasta (slideshow).
 */

import { sendRequest } from "../../utils/request.js";

export async function loadSlideshowAccess(slideshowId) {
  const response = await sendRequest(`/admin/media/${slideshowId}/access`);
  return response.data;
}
