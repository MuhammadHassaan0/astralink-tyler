(() => {
  let usesLeft = 3;
  const textInput   = document.getElementById('textInput');
  const sendBtn     = document.getElementById('sendBtn');
  const log         = document.getElementById('messageLog');
  const waitlistScr = document.getElementById('waitlist-screen');
  const thinking    = document.getElementById('thinking');
  const emailInput  = document.getElementById('emailInput');
  const joinBtn     = document.getElementById('joinBtn');

  // Core send/chat flow
  async function handleSend() {
    const msg = textInput.value.trim();
    if (!msg) return;

    // 1) Append user message
    const u = document.createElement('div');
    u.textContent = msg;
    u.className   = 'text-right text-[#181410]';
    log.append(u);

    // 2) Free-use guard
    usesLeft--;
    if (usesLeft < 0) {
      waitlistScr.classList.remove('hidden');
      return;
    }

    // 3) Disable UI + show spinner
    sendBtn.disabled = true;
    textInput.disabled = true;
    thinking.classList.remove('hidden');

    let payload;
    try {
      // 4) Call backend
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({message: msg})
      });
      if (!res.ok) throw new Error(await res.text());
      payload = await res.json();
    } catch (err) {
      console.error('API Error:', err);
      // hide spinner and re-enable
      thinking.classList.add('hidden');
      sendBtn.disabled = false;
      textInput.disabled = false;
      return;
    }

    // 5) Hide spinner
    thinking.classList.add('hidden');

    const {reply, audio} = payload;

    // 6) Append Tyler’s reply
    const b = document.createElement('div');
    b.textContent = reply;
    b.className   = 'text-left text-[#181410]';
    log.append(b);

    // 7) Play voice if available
    if (audio) {
      const player = new Audio(audio);
      player.play().catch(console.warn);
    }

    // 8) Re-enable UI + clear input
    sendBtn.disabled = false;
    textInput.disabled = false;
    textInput.value = '';
    textInput.focus();
  }

  // Bind handlers once
  sendBtn.addEventListener('click', handleSend);
  textInput.addEventListener('keyup', e => {
    if (e.key === 'Enter') handleSend();
  });

  // Waitlist / join logic stays as before
  joinBtn.addEventListener('click', () => {
    const email = emailInput.value.trim();
    if (!email) return alert('Please enter your email.');
    // → TODO: POST to your Formspree or backend endpoint
    alert(`Thanks! You’ll be notified at ${email}`);
    waitlistScr.classList.add('hidden');
  });
})();

