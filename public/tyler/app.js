(() => {
  let usesLeft = 3;
  const textInput   = document.getElementById('textInput');
  const sendBtn     = document.getElementById('sendBtn');
  const log         = document.getElementById('messageLog');
  const waitlistScr = document.getElementById('waitlist-screen');
  const thinking    = document.getElementById('thinking');
  const emailInput  = document.getElementById('emailInput');
  const joinBtn     = document.getElementById('joinBtn');

  // Send / Chat
  sendBtn.addEventListener('click', async () => {
    const msg = textInput.value.trim();
    if (!msg) return;

    // 1) show user
    const u = document.createElement('div');
    u.textContent = msg;
    u.className   = 'text-right text-[#181410]';
    log.append(u);

    // 2) out of freebies?
    usesLeft--;
    if (usesLeft < 0) {
      waitlistScr.classList.remove('hidden');
      return;
    }

    // 3) show thinking
    thinking.classList.remove('hidden');

    // 4) call API
    let payload;
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({message: msg})
      });
      if (!res.ok) throw new Error(await res.text());
      payload = await res.json();
    } catch (err) {
      console.error('API Error:', err);
      thinking.classList.add('hidden');
      return;
    }

    const {reply, audio} = payload;

    // 5) hide thinking
    thinking.classList.add('hidden');

    // 6) show Tyler’s reply
    const b = document.createElement('div');
    b.textContent = reply;
    b.className   = 'text-left text-[#181410]';
    log.append(b);

    // 7) play voice if present
    if (audio) new Audio(audio).play().catch(console.warn);

    textInput.value = '';
  });

  // Enter key triggers send
  textInput.addEventListener('keyup', e => {
    if (e.key === 'Enter') sendBtn.click();
  });

  // Waitlist join
  joinBtn.addEventListener('click', () => {
    const email = emailInput.value.trim();
    if (!email) return alert('Please enter your email.');
    // TODO: POST to your /api/waitlist or Formspree endpoint
    alert(`Thanks! You’ll be notified at ${email}`);
    waitlistScr.classList.add('hidden');
  });
})();

