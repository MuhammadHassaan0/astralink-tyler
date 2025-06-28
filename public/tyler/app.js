let remaining = 3
const dots = document.querySelectorAll('.dot')
const micBtn = document.getElementById('micBtn')
const sendBtn = document.getElementById('sendBtn')
const payBtn = document.getElementById('payBtn')
const closeModal = document.getElementById('closeModal')
const overlay = document.getElementById('overlay')
const modal = document.getElementById('paymentModal')
const msgBox = document.getElementById('messages')
const input = document.getElementById('textInput')

// Update UI dots
function refreshProgress(){
  dots.forEach((d,i)=> d.classList.toggle('filled', i < remaining))
  document.getElementById('remaining').innerText = remaining
}

// Show payment modal
function showPayModal(){
  overlay.classList.remove('hidden')
  modal.classList.remove('hidden')
}

// Hide payment modal
closeModal.onclick = () => {
  overlay.classList.add('hidden')
  modal.classList.add('hidden')
}

// PayPal redirect
payBtn.onclick = () => {
  window.location.href = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YOUR_BUTTON_ID'
}

// Send text question
sendBtn.onclick = askQuestion
micBtn.onclick  = askQuestion // for now: same behavior

async function askQuestion(){
  if (remaining <= 0) return showPayModal()
  const msg = input.value.trim()
  if (!msg) return
  appendMessage('You', msg)
  input.value = ''
  remaining--
  refreshProgress()

  const res = await fetch('/api/chat', {
    method:'POST',
    headers:{ 'Content-Type':'application/json' },
    body: JSON.stringify({ message: msg })
  })
  const { reply } = await res.json()
  appendMessage('Coach Tyler', reply)

  if (remaining <= 0) showPayModal()
}

function appendMessage(who, text){
  const div = document.createElement('div')
  div.className = who === 'You' ? 'user' : 'bot'
  div.innerText = text
  msgBox.appendChild(div)
  msgBox.scrollTop = msgBox.scrollHeight
}

refreshProgress()

