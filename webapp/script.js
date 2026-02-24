const buyBtn = document.getElementById("buyBtn");
buyBtn.addEventListener("click", () => {
    if(window.Telegram.WebApp){
        Telegram.WebApp.sendData(JSON.stringify({action:"buy", amount:100}));
        alert("Данные отправлены боту!");
    } else {
        alert("Открыто не через Telegram!");
    }
});
