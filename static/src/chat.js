let chatbox = document.getElementById("chatbox")
let isShiftDown = false;
let username = document.getElementById("usernameField")

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
