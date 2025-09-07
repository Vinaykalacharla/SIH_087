document.addEventListener('DOMContentLoaded', () => {
  // Camera capture and upload
  const camBtn = document.getElementById('cameraBtn');
  const video = document.getElementById('cameraStream');
  const canvas = document.getElementById('snapCanvas');
  if (camBtn) {
    camBtn.addEventListener('click', async () => {
      if (video.classList.contains('hidden')) {
        video.classList.remove('hidden');
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ video: true });
          video.srcObject = stream;
          camBtn.textContent = 'Capture Photo';
        } catch (e) {
          alert('Camera access failed: ' + e.message);
        }
      } else {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        const dataUrl = canvas.toDataURL('image/jpeg');
        const blob = await (await fetch(dataUrl)).blob();
        const fd = new FormData();
        fd.append('image', blob, 'capture.jpg');
        const res = await fetch('/upload-pest', { method: 'POST', body: fd });
        if (res.redirected) window.location = res.url;
        else {
          const text = await res.text();
          document.body.innerHTML = text;
        }
      }
    });
  }

  // Dark mode toggle
  const darkModeToggle = document.getElementById('darkModeToggle');
  const darkModeIcon = document.getElementById('darkModeIcon');
  if (darkModeToggle && darkModeIcon) {
    // Initialize dark mode based on localStorage
    if (localStorage.getItem('darkMode') === 'enabled') {
      document.body.classList.add('dark-mode');
      darkModeIcon.classList.remove('fa-moon');
      darkModeIcon.classList.add('fa-sun');
    }

    darkModeToggle.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      const isDark = document.body.classList.contains('dark-mode');
      if (isDark) {
        darkModeIcon.classList.remove('fa-moon');
        darkModeIcon.classList.add('fa-sun');
        localStorage.setItem('darkMode', 'enabled');
      } else {
        darkModeIcon.classList.remove('fa-sun');
        darkModeIcon.classList.add('fa-moon');
        localStorage.setItem('darkMode', 'disabled');
      }
    });
  }

  // Mobile menu toggle
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });
  }
});
