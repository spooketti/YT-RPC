const servers = {
    iceServers: [
        {
            urls: [
                "stun:stun.l.google.com:19302",
                "stun:stun.l.google.com:5349",
                "stun:stun1.l.google.com:3478",
                "stun:stun1.l.google.com:5349",
                "stun:stun2.l.google.com:19302",
                "stun:stun2.l.google.com:5349",
                "stun:stun3.l.google.com:3478",
                "stun:stun3.l.google.com:5349",
                "stun:stun4.l.google.com:19302",
                "stun:stun4.l.google.com:5349"
            ],
        },
    ],
    iceCandidatePoolSize: 10,
};

const socket = new WebSocket("wss://yt-rpc.onrender.com");
let videoStreamGlobal;
let globalPeer;

socket.onmessage = async function (event) {
    const messageData = JSON.parse(event.data);
    switch (messageData["context"]) {
        case "viewerAcceptServer":
            viewerAcceptServer(messageData);
            break;
        case "iceToViewerServer":
            globalPeer.addIceCandidate(new RTCIceCandidate(JSON.parse(messageData["candidate"])));
        break;
        case "artUpdate":
            document.getElementById("albumCover").src = messageData["imageURL"]
            document.getElementById("songTitle").innerText = messageData["title"]
            document.getElementById("songArtist").innerText = messageData["artist"]
        break;
        case "chatSTC":
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
            break;
    }
};

function sendMessage(message) {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(message));
    } else {
        console.error("WebSocket connection is not open.");
    }
}

function viewerAcceptServer(messageData) {
    let remotedesc = new RTCSessionDescription({
        type: "answer",
        sdp: messageData["sdp"]
    });

    globalPeer.ontrack = (event) => {
        console.log("Track received:", event.track.kind);
        document.getElementById("videoElement").srcObject = event.streams[0];
        const button = document.getElementById("ConnectButton");
        if (button) button.remove();
    };

    if (globalPeer.signalingState === "stable") {
        console.warn("Skipping setRemoteDescription because connection is already stable.");
        return;
    }

    globalPeer.setRemoteDescription(remotedesc)
        .then(() => {
            console.log("Remote description set successfully.");
        })
        .catch(error => {
            console.error("Failed to set remote description:", error);
        });
}

async function watch() {
    const peer = new RTCPeerConnection(servers);
    peer.addTransceiver("video", {direction:"recvonly"})
    peer.addTransceiver("audio", { direction: "recvonly" });
    const offer = await peer.createOffer();
    await peer.setLocalDescription(offer);
    
    peer.onicecandidate = (e) => {
        if (e.candidate) {
            sendMessage({ context: "iceToStreamerClient", candidate: JSON.stringify(e.candidate.toJSON()) });
        }
    };
    
    globalPeer = peer;
    sendMessage({ context: "viewerOfferClient", sdp: offer.sdp });
}

socket.onerror = function (error) {
    console.error("WebSocket error: ", error);
};

socket.onclose = function (event) {
    console.log("WebSocket connection closed:", event);
};

socket.onopen = function (event) {
    console.log("WebSocket connection established.");
};