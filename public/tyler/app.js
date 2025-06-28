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
let remaining = 3
const fill = document.querySelector('.progress__fill')
const micBtn   = document.getElementById('micBtn')
const sendBtn  = document.getElementById('sendBtn')
const payBtn   = document.getElementById('payBtn')
const closeModal = document.getElementById('closeModal')
const overlay  = document.getElementById('overlay')
const modal    = document.getElementById('paymentModal')
const msgs     = document.getElementById('messages')
const input    = document.getElementById('textInput')

// animate progress
function updateProgress() {
  fill.style.transform = `scaleX(${remaining/3})`
}
updateProgress()

// show / hide paywall
function showPay()  { overlay.classList.remove('hidden'); modal.classList.remove('hidden') }
function hidePay()  { overlay.classList.add('hidden');    modal.classList.add('hidden') }

// ask question
async function ask(q) {
  if (remaining <= 0) return showPay()
  const divYou = document.createElement('div')
  divYou.className = 'bubble user'
  divYou.textContent = q
  msgs.appendChild(divYou)
  msgs.scrollTop = msgs.scrollHeight

  remaining--
  updateProgress()

  const res = await fetch('/api/chat', {
    method:'POST',
    headers:{ 'Content-Type':'application/json' },
    body: JSON.stringify({ message: q })
  })
  const { reply } = await res.json()
  const divBot = document.createElement('div')
  divBot.className = 'bubble bot'
  divBot.textContent = reply
  msgs.appendChild(divBot)
  msgs.scrollTop = msgs.scrollHeight

  if (remaining <= 0) showPay()
}

// event handlers
sendBtn.onclick = () => {
  const text = input.value.trim()
  if (!text) return
  input.value = ''
  ask(text)
}
micBtn.onclick = () => {
  // TODO: hook up Web Speech API…
  alert('🎤 voice not yet live!')
}
closeModal.onclick = hidePay
payBtn.onclick   = () => {
  location.href = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YOUR_BTN_ID'
}

