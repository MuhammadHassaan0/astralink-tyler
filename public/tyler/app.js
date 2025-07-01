(() => {
  let usesLeft = 3;

  const textInput     = document.getElementById('textInput');
  const sendBtn       = document.getElementById('sendBtn');
  const log           = document.getElementById('messageLog');
  const chatScreen    = document.getElementById('chat-screen');
  const waitlistScr   = document.getElementById('waitlist-screen');

  sendBtn.addEventListener('click', async () => {
    const msg = textInput.value.trim();
    if (!msg) return;

    // show user message
    const u = document.createElement('div');
    u.textContent = msg;
    u.className = 'text-right text-[#181410]';
    log.append(u);

    // decrement free uses
    usesLeft--;
    if (usesLeft < 0) {
      // lock chat & show waitlist
      waitlistScr.classList.remove('hidden');
      return;
    }

    // call your chat API endpoint
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type':'application/json' },
        body: JSON.stringify({ message: msg })
      });
      const { reply } = await res.json();

      const b = document.createElement('div');
      b.textContent = reply;
      b.className = 'text-left text-[#181410]';
      log.append(b);
    } catch (err) {
      console.error(err);
      const errDiv = document.createElement('div');
      errDiv.textContent = '⚠️ Something went wrong.';
      errDiv.className = 'text-left text-red-600';
      log.append(errDiv);
    }

    textInput.value = '';
  });

  // allow pressing Enter key to submit
  textInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') sendBtn.click();
  });
})();

