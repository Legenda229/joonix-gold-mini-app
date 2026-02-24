const tg = window.Telegram.WebApp;
tg.expand();

function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

function buyGold() {
  const amount = document.getElementById('goldInput').value;
  tg.sendData(JSON.stringify({ action: "buy", gold: amount }));
  tg.showAlert("Заявка отправлена в бот.");
}
