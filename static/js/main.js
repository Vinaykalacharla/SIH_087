// main.js (camera capture and upload)
document.addEventListener('DOMContentLoaded', ()=>{
  const camBtn = document.getElementById('cameraBtn');
  const video = document.getElementById('cameraStream');
  const canvas = document.getElementById('snapCanvas');
  if (!camBtn) return;
  camBtn.addEventListener('click', async ()=>{
    if (video.classList.contains('hidden')){
      video.classList.remove('hidden');
      try{
        const stream = await navigator.mediaDevices.getUserMedia({video:true});
        video.srcObject = stream;
        camBtn.textContent = 'Capture Photo';
      }catch(e){
        alert('Camera access failed: ' + e.message);
      }
    } else {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video,0,0);
      const dataUrl = canvas.toDataURL('image/jpeg');
      const blob = await (await fetch(dataUrl)).blob();
      const fd = new FormData();
      fd.append('image', blob, 'capture.jpg');
      const res = await fetch('/upload-pest',{method:'POST', body: fd});
      if (res.redirected) window.location = res.url; else {
        const text = await res.text();
        document.body.innerHTML = text;
      }
    }
  });
});
