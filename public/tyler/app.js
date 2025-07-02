(() => {
  let usesLeft = 3;
  const textInput   = document.getElementById('textInput');
  const sendBtn     = document.getElementById('sendBtn');
  const log         = document.getElementById('messageLog');
  const waitlistScr = document.getElementById('waitlist-screen');

  sendBtn.addEventListener('click', async () => {
    const msg = textInput.value.trim();
    if (!msg) return;

    // 1) append user message
    const u = document.createElement('div');
    u.textContent = msg;
    u.className   = 'text-right text-[#181410]';
    log.append(u);

    // 2) free-use check
    usesLeft--;
    if (usesLeft < 0) {
      waitlistScr.classList.remove('hidden');
      return;
    }

    // 3) call chat + TTS endpoint
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message: msg})
    });
    if (!res.ok) {
      console.error('Chat API error', await res.text());
      return;
    }
    const {reply, audio} = await res.json();

    // 4) append Tyler’s text reply
    const b = document.createElement('div');
    b.textContent = reply;
    b.className   = 'text-left text-[#181410]';
    log.append(b);

    // 5) play Tyler’s voice if provided
    if (audio) {
      const player = new Audio(audio);
      player.play().catch(console.warn);
    }

    // clear input
    textInput.value = '';
  });

  // also send on Enter
  textInput.addEventListener('keyup', e => {
    if (e.key === 'Enter') sendBtn.click();
  });
})();

