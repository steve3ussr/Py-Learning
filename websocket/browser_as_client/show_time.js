window.addEventListener("DOMContentLoaded", () => {
  const ordered_list = document.createElement("ol");
  document.body.appendChild(ordered_list);

  const websocket = new WebSocket("ws://localhost:6789/");
  websocket.onmessage = ({ data }) => {
    const message = document.createElement("li");
    const content = document.createTextNode(data);
    message.appendChild(content);
    ordered_list.appendChild(message);
  };
});