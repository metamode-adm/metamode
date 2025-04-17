// static/js/media/actions/enhance_videos.js

export function enhanceVideos() {
    document.querySelectorAll("video").forEach((video) => {
      video.playbackRate = 2.0;
    });
  }
  