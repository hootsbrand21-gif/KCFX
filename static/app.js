const socket = io();

socket.on("kcf_signal", (data)=>{
  const div = document.createElement("div");
  div.innerHTML = `<p>${data.time} — ${data.direction} ${data.symbol} @${data.entry}
                   (SL:${data.stop_loss}, TP:${data.take_profit}) Conf:${data.confidence}</p>`;
  document.getElementById("signals").prepend(div);
});

function analyze(){
  fetch("/analyze", {method:"POST"})
    .then(r=>r.json())
    .then(d=>console.log("Analysis:", d));
}
