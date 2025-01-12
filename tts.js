const textInput = document.getElementById('text-input');
const convertBtn = document.getElementById('convert-btn');
const stopBtn = document.getElementById('stop-btn');

let speechSynthesis = window.speechSynthesis;
let speechSynthesisUtterance = new SpeechSynthesisUtterance();

function setIndianEnglishVoice() {
    let voices = speechSynthesis.getVoices();
    let indianVoice = voices.find(voice => voice.lang.includes('en-IN'));
    speechSynthesisUtterance.voice = indianVoice || voices[0];  
}

speechSynthesis.onvoiceschanged = setIndianEnglishVoice;

convertBtn.addEventListener('click', () => {
    let text = textInput.value.trim();
    if (text !== '') {
        speechSynthesisUtterance.text = text;
        speechSynthesisUtterance.pitch = 1.1;  // Adjust pitch for a more feminine sound
        speechSynthesisUtterance.rate = 1.0;   // Normal speaking rate
        speechSynthesisUtterance.volume = 1.0; // Full volume

        speechSynthesis.speak(speechSynthesisUtterance);
        convertBtn.disabled = true;
        stopBtn.disabled = false;
    }
});

stopBtn.addEventListener('click', () => {
    speechSynthesis.cancel();
    convertBtn.disabled = false;
    stopBtn.disabled = true;
});
