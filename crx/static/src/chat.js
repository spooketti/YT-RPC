let chatbox = document.getElementById("chatbox")
let isShiftDown = false;
let username = document.getElementById("usernameField")
const socket = new WebSocket("wss://yt-rpc.onrender.com");
socket.onmessage = async function (event) {
    const messageData = JSON.parse(event.data);
    if (messageData["context"] == "chatSTC") {
        createMessage(messageData)
    }
};

document.addEventListener("keydown", function (e) {
    switch (e.key) {
        case "Shift":
            isShiftDown = true;
            break;

        case "Enter":
            if (!isShiftDown) {
                e.preventDefault()
                postMessage()
            }
            break;
    }
})

document.addEventListener("keyup", function (e) {
    switch (e.key) {
        case "Shift":
            isShiftDown = false;
            break;
    }
})

function postMessage() {
    let payload = {
        context: "chatCTS",
        username: username.value,
        message: chatbox.value
    }
    sendMessage(payload); //Client to Server
    chatbox.value = "";
}

function sendMessage(message) {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(message));
    } else {
        console.error("WebSocket connection is not open.");
    }
}

function createMessage(messageData) {
    let chatbody = document.getElementById("chatBody")
    let messageWrapper = document.createElement("div")
    messageWrapper.classList.add("chatMessage")
    let chatUN = document.createElement("span")
    chatUN.classList.add("chatUN")
    chatUN.textContent = `${messageData["username"]}:`
    chatUN.style.color = messageData["color"]
    let chatMSG = document.createElement("span")
    chatMSG.classList.add("chatMSG")
    chatMSG.textContent = messageData["message"]
    messageWrapper.appendChild(chatUN)
    messageWrapper.appendChild(chatMSG)
    chatbody.appendChild(messageWrapper)
}