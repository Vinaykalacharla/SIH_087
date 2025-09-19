// Dashboard chatbot functionality
document.addEventListener('DOMContentLoaded', () => {
  const chatMessages = document.getElementById('chat-messages');
  const chatInput = document.getElementById('chat-input');
  const sendMessageBtn = document.getElementById('send-message');
  const chatLanguage = document.getElementById('chat-language');

  // Make chatbot sidebar draggable
  const chatbotSidebar = document.getElementById('chatbot-sidebar');
  let isDragging = false;
  let dragOffsetX = 0;
  let dragOffsetY = 0;

  chatbotSidebar.style.position = 'fixed';

  chatbotSidebar.addEventListener('mousedown', (e) => {
    if (e.target.id === 'close-chatbot' || e.target.closest('#close-chatbot')) {
      return; // Don't drag when clicking close button
    }
    isDragging = true;
    dragOffsetX = e.clientX - chatbotSidebar.getBoundingClientRect().left;
    dragOffsetY = e.clientY - chatbotSidebar.getBoundingClientRect().top;
    chatbotSidebar.style.transition = 'none'; // Disable transition while dragging
  });

  document.addEventListener('mouseup', () => {
    isDragging = false;
    chatbotSidebar.style.transition = ''; // Re-enable transition
  });

  document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    let newLeft = e.clientX - dragOffsetX;
    let newTop = e.clientY - dragOffsetY;

    // Constrain within viewport
    const maxLeft = window.innerWidth - chatbotSidebar.offsetWidth;
    const maxTop = window.innerHeight - chatbotSidebar.offsetHeight;
    newLeft = Math.min(Math.max(0, newLeft), maxLeft);
    newTop = Math.min(Math.max(0, newTop), maxTop);

    chatbotSidebar.style.left = newLeft + 'px';
    chatbotSidebar.style.top = newTop + 'px';
    chatbotSidebar.style.right = 'auto'; // Override right positioning
    chatbotSidebar.style.bottom = 'auto'; // Override bottom positioning
  });

  function appendMessage(text, cls = 'bot') {
    const el = document.createElement('div');
    el.className = cls === 'user' ? 'bg-blue-100 p-3 rounded-lg mb-2 ml-8' : 'bg-gray-100 p-3 rounded-lg mb-2 mr-8';
    el.innerHTML = `<p class="text-sm">${text}</p>`;
    chatMessages.appendChild(el);
    // Scroll to bottom smoothly
    chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
    // Allow scrolling up by not forcing scroll if user has scrolled up
  }

  // Prevent auto scroll if user scrolls up manually
  let userScrolled = false;
  chatMessages.addEventListener('scroll', () => {
    const threshold = 20; // px from bottom to consider as bottom
    const position = chatMessages.scrollTop + chatMessages.clientHeight;
    const height = chatMessages.scrollHeight;
    userScrolled = position < height - threshold;
  });

  function appendMessageWithScroll(text, cls = 'bot') {
    const el = document.createElement('div');
    el.className = cls === 'user' ? 'bg-blue-100 p-3 rounded-lg mb-2 ml-8' : 'bg-gray-100 p-3 rounded-lg mb-2 mr-8';
    el.innerHTML = `<p class="text-sm">${text}</p>`;
    chatMessages.appendChild(el);
    if (!userScrolled) {
      chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
    }
  }

  if (sendMessageBtn && chatInput && chatMessages) {
    sendMessageBtn.onclick = async () => {
      const message = chatInput.value.trim();
      const locale = chatLanguage ? chatLanguage.value : 'en';
      if (!message) return;

      appendMessageWithScroll(message, 'user');
      chatInput.value = '';
      appendMessageWithScroll('Thinking...', 'bot');

      try {
        const res = await fetch('/chatbot/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message, lang: locale })
        });
        const data = await res.json();

        // Remove "Thinking..." message
        const lastBotMessage = chatMessages.querySelector('.bg-gray-100:last-child');
        if (lastBotMessage && lastBotMessage.textContent.includes('Thinking...')) {
          lastBotMessage.remove();
        }

        if (data.error) appendMessageWithScroll('Error: ' + data.error, 'bot');
        else appendMessageWithScroll(data.answer_final || data.answer, 'bot');
      } catch (e) {
        // Remove "Thinking..." message
        const lastBotMessage = chatMessages.querySelector('.bg-gray-100:last-child');
        if (lastBotMessage && lastBotMessage.textContent.includes('Thinking...')) {
          lastBotMessage.remove();
        }
        appendMessageWithScroll('Network error', 'bot');
      }
    };

    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') sendMessageBtn.click();
    });
  }
});
