const chat = document.getElementById('chat')
const msgBox = document.getElementById('message')
const sendBtn = document.getElementById('send')
const langSel = document.getElementById('lang')

function appendMessage(text, cls='bot'){
  const el = document.createElement('div')
  el.className = 'msg ' + cls
  el.textContent = text
  chat.appendChild(el)
  chat.scrollTop = chat.scrollHeight
}

sendBtn.onclick = async () => {
  const message = msgBox.value.trim()
  const locale = langSel.value === 'auto' ? null : langSel.value
  if(!message) return
  appendMessage(message, 'user')
  msgBox.value = ''
  appendMessage('Thinking...', 'bot')

  try{
    const res = await fetch('/api/chat', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message, lang: locale})
    })
    const data = await res.json()
    const last = chat.querySelectorAll('.msg.bot')
    if(last.length) last[last.length-1].remove()

    if(data.error) appendMessage('Error: ' + data.error, 'bot')
    else appendMessage(data.answer_final || data.answer, 'bot')
  }catch(e){
    appendMessage('Network error', 'bot')
  }
}

msgBox.addEventListener('keydown', (e)=>{if(e.key==='Enter') sendBtn.click()})
