window.addEventListener("DOMContentLoaded", () => {

  const websocket = new WebSocket("ws://1.1.1.1:6789/");
  const input_dialog = document.getElementById('message-input');
  const chat_browser = document.getElementById('chat-display');
  const send_button = document.getElementById('send-button');

  window.addEventListener('beforeunload', function(event)  {
    websocket.send(JSON.stringify({ type: 'close-or-refresh'}));
    websocket.close();
    
  });

  function fill_name(status, websocket) {
    while(1) {
      
      switch (status) {
        case "un-registered":
          var username =  window.prompt("Please enter a username");
          break;
        case "duplicated name":
          var username =  window.prompt("Name duplicated, please enter another username");
          break;
      }

      if (username == null) {
        websocket.send(JSON.stringify({client_cancel: ''}));
        window.close();
      }

      if (username.trim() == '') {
        console.log(`empty name: ${username}`); 
        continue;
      }

      websocket.send(JSON.stringify({username: username}));
      break;
    }
  }

  function send_msg() {
    let user_msg = input_dialog.value.trim();
    console.log(`user try to send: ${user_msg}`);
    if (user_msg) {
      websocket.send(JSON.stringify({ type: 'send', msg: user_msg }));
      // Scroll to the bottom
      // chat_browser.scrollTop = chat_browser.scrollHeight;
      window.scrollTo(0, document.body.scrollHeight);
      input_dialog.value = '';
    }
  }

  function disp_msg(msg) {
    // Add the message to the chat display
    const messageElement = document.createElement('div');
    messageElement.textContent = msg;
    chat_browser.appendChild(messageElement);
  }


  // Event listener for send button
  send_button.addEventListener('click', send_msg);

  // Event listener for Enter key in the input box
  input_dialog.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {send_msg();}
  });

  websocket.onmessage = ({ data }) => {
    const event = JSON.parse(data);

    switch (event.type) {
      case "alert_and_quit":
        let alert_content = event.msg;
        window.alert(alert_content);
        window.close();
        break;

      case "req_username":
        fill_name(event.status, websocket);
        break;

      case "sys_broadcast":
        let sys_msg = event.msg;
        let user_cnt = event.cnt;
        disp_msg(sys_msg);
        break;

      case "user_broadcast":
        let user_msg = event.msg;
        disp_msg(user_msg);
        break;

      default:
        console.error("unsupported event", event);
    }
  };
});


