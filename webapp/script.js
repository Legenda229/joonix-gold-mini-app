const tg = window.Telegram.WebApp;
tg.expand();

function buyGold(){
  const gold = document.getElementById("goldInput").value;
  tg.sendData(JSON.stringify({gold: gold}));
  tg.showAlert("Заявка отправлена!");
}
