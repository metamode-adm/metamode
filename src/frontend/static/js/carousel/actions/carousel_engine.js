/**
 * Controla o carrossel de mídias: navegação, tempo e vídeos.
 */
export function startCarousel() {
    const items = document.querySelectorAll(".carousel-item");
    const progressBar = document.getElementById("progress-bar");
    let currentIndex = 0;
    let autoPlayTimer = null;
  
    async function getMediaDuration() {
      const currentItem = items[currentIndex];
      const video = currentItem.querySelector("video");
      if (video) {
        return new Promise(resolve => {
          if (video.readyState >= 3) resolve(video.duration * 1000);
          else video.addEventListener("canplay", () => resolve(video.duration * 1000), { once: true });
        });
      }
      return parseInt(currentItem.dataset.duration) * 1000 || 5000;
    }
  
    async function showSlide(index) {
      const currentItem = items[index];
      const video = currentItem.querySelector("video");
      const img = currentItem.querySelector("img");
  
      items.forEach((item, i) => {
        item.classList.toggle("active", i === index);
        const itemVideo = item.querySelector("video");
        if (itemVideo && i !== index) {
          itemVideo.pause();
          itemVideo.currentTime = 0;
          itemVideo.style.visibility = "hidden";
        }
      });
  
      if (img) img.style.visibility = "visible";
      if (video) {
        video.style.visibility = "visible";
        try {
          await new Promise((resolve, reject) => {
            if (video.readyState >= 3) resolve();
            else {
              video.addEventListener("canplay", resolve, { once: true });
              video.addEventListener("error", reject, { once: true });
            }
          });
          video.currentTime = 0;
          await video.play();
          video.onended = () => setTimeout(nextSlide, 200);
          video.onerror = nextSlide;
        } catch {
          nextSlide();
        }
      } else {
        startAutoPlay(await getMediaDuration());
      }
  
      updateProgressBar(await getMediaDuration());
      const next = items[(index + 1) % items.length]?.querySelector("video");
      if (next && next.readyState === 0) next.load();
    }
  
    function updateProgressBar(duration) {
      progressBar.style.transition = "none";
      progressBar.style.width = "0%";
      setTimeout(() => {
        progressBar.style.transition = `width linear ${duration / 1000}s`;
        progressBar.style.width = "100%";
      }, 50);
    }
  
    function startAutoPlay(duration) {
      clearTimeout(autoPlayTimer);
      autoPlayTimer = setTimeout(nextSlide, duration);
    }
  
    function nextSlide() {
      currentIndex = (currentIndex + 1) % items.length;
      showSlide(currentIndex);
    }
  
    showSlide(currentIndex);
  }
  