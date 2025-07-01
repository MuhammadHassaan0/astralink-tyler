(() => {
  let usesLeft = 3;
  const textInput   = document.getElementById('textInput');
  const sendBtn     = document.getElementById('sendBtn');
  const log         = document.getElementById('messageLog');
  const waitlistScr = document.getElementById('waitlist-screen');
  const emailInput  = document.getElementById('emailInput');
  const joinBtn     = document.getElementById('joinBtn');

  sendBtn.addEventListener('click', async () => {
    const msg = textInput.value.trim();
    if (!msg) return;

    // show user message
    const u = document.createElement('div');
    u.textContent = msg;
    u.className   = 'text-right text-[#181410]';
    log.append(u);

    if (usesLeft <= 0) {
      // lock out and show waitlist
      waitlistScr.classList.remove('hidden');
      return;
    }
    usesLeft--;

    // call your Vercel chat endpoint
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message: msg})
    });
    const {reply} = await res.json();

    const b = document.createElement('div');
    b.textContent = reply;
    b.className   = 'text-left text-[#181410]';
    log.append(b);

    textInput.value = '';
  });

  joinBtn.addEventListener('click', () => {
    const email = emailInput.value.trim();
    if (!email) return alert('Please enter your email.');
    // TODO: wire this up to your backend / Zapier / Google Sheet
    alert(`Thanks! You’ll be notified at ${email}`);
    waitlistScr.classList.add('hidden');
  });
})();

