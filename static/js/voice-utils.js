// Voice Utilities for microphone (speech recognition) and speaker (speech synthesis)

export function startSpeechRecognition(lang = 'en-IN', onResult, onError) {
  console.log('Starting speech recognition...');
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    console.error('Speech recognition not supported');
    alert('Speech recognition not supported in this browser.');
    return;
  }
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.lang = lang;
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (event) => {
    console.log('Speech recognition result:', event);
    const speechResult = event.results[0][0].transcript.trim();
    console.log('Transcript:', speechResult);
    if (onResult) onResult(speechResult);
  };

  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    if (onError) onError(event.error);
    else alert('Speech recognition error: ' + event.error);
  };

  recognition.onstart = () => {
    console.log('Speech recognition started');
  };

  recognition.onend = () => {
    console.log('Speech recognition ended');
  };

  try {
    recognition.start();
    console.log('Speech recognition start() called');
  } catch (error) {
    console.error('Error starting speech recognition:', error);
    alert('Error starting speech recognition: ' + error.message);
  }
}

export function speakText(text) {
  console.log('Speaking text:', text);
  if (!('speechSynthesis' in window)) {
    console.error('Speech synthesis not supported');
    alert('Speech synthesis not supported in this browser.');
    return;
  }

  // Cancel any ongoing speech
  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'en-IN'; // Set language for better pronunciation
  utterance.rate = 0.8; // Slightly slower for clarity
  utterance.pitch = 1;

  utterance.onstart = () => {
    console.log('Speech synthesis started');
  };

  utterance.onend = () => {
    console.log('Speech synthesis ended');
  };

  utterance.onerror = (event) => {
    console.error('Speech synthesis error:', event);
  };

  try {
    window.speechSynthesis.speak(utterance);
    console.log('Speech synthesis speak() called');
  } catch (error) {
    console.error('Error in speech synthesis:', error);
    alert('Error in speech synthesis: ' + error.message);
  }
}
