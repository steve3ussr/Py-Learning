window.addEventListener("DOMContentLoaded", () => {
  const websocket = new WebSocket("ws://localhost:6789/");

  document.querySelector(".minus").addEventListener("click", () => {
    websocket.send(JSON.stringify({ key: "minus" }));
  });

  document.querySelector(".plus").addEventListener("click", () => {
    websocket.send(JSON.stringify({ key: "plus" }));
  });

  websocket.onmessage = ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "cnt":
        document.querySelector(".cnt").textContent = event.value;
        break;
      case "users":
        const users = `${event.count} user${event.count == 1 ? "" : "s"}`;
        document.querySelector(".users").textContent = users;
        break;
      default:
        console.error("unsupported event", event);
    }
  };
});