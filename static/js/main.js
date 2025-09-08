import { startSpeechRecognition, speakText } from './voice-utils.js';

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

  // Voice control popup
  const voiceControlPopup = document.getElementById('voiceControlPopup');
  const closeVoicePopupBtn = document.getElementById('closeVoicePopupBtn');

  // Voice control buttons in popup
  const popupMicrophoneBtn = document.getElementById('popupMicrophoneBtn');
  const popupMicrophoneIcon = document.getElementById('popupMicrophoneIcon');
  const popupSpeakerBtn = document.getElementById('popupSpeakerBtn');
  const popupSpeakerIcon = document.getElementById('popupSpeakerIcon');

  console.log('Voice popup elements found:', {
    voiceControlPopup,
    popupMicrophoneBtn,
    popupMicrophoneIcon,
    popupSpeakerBtn,
    popupSpeakerIcon
  });

  // Show voice popup after a delay or on user interaction
  setTimeout(() => {
    if (voiceControlPopup) {
      voiceControlPopup.classList.remove('hidden');
      console.log('Voice popup shown');
    }
  }, 2000); // Show after 2 seconds

  // Close popup button
  if (closeVoicePopupBtn) {
    closeVoicePopupBtn.addEventListener('click', () => {
      if (voiceControlPopup) {
        voiceControlPopup.classList.add('hidden');
        console.log('Voice popup hidden');
      }
    });
  }

  // Popup microphone button
  if (popupMicrophoneBtn && popupMicrophoneIcon) {
    console.log('Setting up popup microphone button listener');
    let recognizing = false;

    popupMicrophoneBtn.addEventListener('click', () => {
      console.log('Popup microphone button clicked, recognizing:', recognizing);
      if (!recognizing) {
        recognizing = true;
        popupMicrophoneIcon.classList.add('text-red-400');
        console.log('Starting speech recognition...');
        startSpeechRecognition('en-IN', (result) => {
          console.log('Speech recognition result:', result);
          recognizing = false;
          popupMicrophoneIcon.classList.remove('text-red-400');
          alert('You said: ' + result);
          // You can add further processing of the speech result here
        }, (error) => {
          console.error('Speech recognition error:', error);
          recognizing = false;
          popupMicrophoneIcon.classList.remove('text-red-400');
          alert('Speech recognition error: ' + error);
        });
      } else {
        console.log('Already recognizing, ignoring click');
      }
    });
  } else {
    console.error('Popup microphone button or icon not found');
  }

  // Popup speaker button
  if (popupSpeakerBtn && popupSpeakerIcon) {
    console.log('Setting up popup speaker button listener');
    let isSpeaking = false;
    let currentUtterance = null;

    popupSpeakerBtn.addEventListener('click', () => {
      console.log('Popup speaker button clicked, isSpeaking:', isSpeaking);
      if (!isSpeaking) {
        // Start speaking
        const pageText = document.body.innerText || document.body.textContent;
        if (pageText.trim()) {
          console.log('Starting to speak page text, length:', pageText.length);
          isSpeaking = true;
          popupSpeakerIcon.classList.remove('fa-volume-up');
          popupSpeakerIcon.classList.add('fa-stop');

          // Create utterance
          currentUtterance = new SpeechSynthesisUtterance(pageText);

          // Handle speech end
          currentUtterance.onend = () => {
            console.log('Speech ended naturally');
            isSpeaking = false;
            popupSpeakerIcon.classList.remove('fa-stop');
            popupSpeakerIcon.classList.add('fa-volume-up');
            currentUtterance = null;
          };

          // Handle speech error
          currentUtterance.onerror = () => {
            console.error('Speech synthesis error');
            isSpeaking = false;
            popupSpeakerIcon.classList.remove('fa-stop');
            popupSpeakerIcon.classList.add('fa-volume-up');
            currentUtterance = null;
          };

          // Start speaking
          window.speechSynthesis.speak(currentUtterance);
        } else {
          console.log('No text to speak');
        }
      } else {
        // Stop speaking
        console.log('Stopping speech');
        if (currentUtterance) {
          window.speechSynthesis.cancel();
          currentUtterance = null;
        }
        isSpeaking = false;
        popupSpeakerIcon.classList.remove('fa-stop');
        popupSpeakerIcon.classList.add('fa-volume-up');
      }
    });
  } else {
    console.error('Popup speaker button or icon not found');
  }

  // Profile sidebar toggle
  const profileBtn = document.getElementById('profileBtn');
  const profileSidebar = document.getElementById('profileSidebar');
  const sidebarOverlay = document.getElementById('sidebarOverlay');
  const closeSidebar = document.getElementById('closeSidebar');

  if (profileBtn && profileSidebar && sidebarOverlay) {
    // Toggle sidebar when profile button is clicked
    profileBtn.addEventListener('click', () => {
      profileSidebar.classList.toggle('open');
      sidebarOverlay.classList.toggle('active');
    });

    // Close sidebar when close button is clicked
    if (closeSidebar) {
      closeSidebar.addEventListener('click', () => {
        profileSidebar.classList.remove('open');
        sidebarOverlay.classList.remove('active');
      });
    }

    // Close sidebar when overlay is clicked
    sidebarOverlay.addEventListener('click', () => {
      profileSidebar.classList.remove('open');
      sidebarOverlay.classList.remove('active');
    });
  }
});
