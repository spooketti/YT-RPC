ws = new WebSocket("ws://localhost:8765")

ws.onopen = () => {
    
};

ws.onmessage = (event) => {
    alert(event.data)
};

ws.onclose = () => {
   
};

let globalPeer

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

socket.onmessage = async function (event) {
    const messageData = JSON.parse(event.data);
    switch (messageData["context"]) {
        case "viewerOfferServer":
            viewerOfferServer(messageData);
            break;
        case "viewerAcceptServer":
            viewerAcceptServer(messageData);
            break;
        case "iceToStreamerServer":
        case "iceToViewerServer":
            globalPeer.addIceCandidate(new RTCIceCandidate(JSON.parse(messageData["candidate"])));
            break;
    }
};

function sendMessage(message) {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(message));
        return
    } 
    console.error("YT-RPC: Websocket not open")
}

async function viewerOfferServer(messageData) {
    const peer = new RTCPeerConnection(servers);
    globalPeer = peer;
    
    let remotedesc = new RTCSessionDescription({
        type: "offer",
        sdp: messageData["sdp"]
    });
    
    peer.onicecandidate = (e) => {
        if (e.candidate) {
            sendMessage({ context: "iceToViewerClient", candidate: JSON.stringify(e.candidate.toJSON()) });
        }
    };
    
    await peer.setRemoteDescription(remotedesc);
    videoStreamGlobal.getTracks().forEach(track => peer.addTrack(track, videoStreamGlobal));
    const answer = await peer.createAnswer();
    await peer.setLocalDescription(answer);
    
    sendMessage({
        context: "viewerAcceptClient",
        sdp: answer.sdp,
        returnID: messageData["returnID"]
    });
}

function viewerAcceptServer(messageData) {
    let remotedesc = new RTCSessionDescription({
        type: "answer",
        sdp: messageData["sdp"]
    });
    
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
    
    globalPeer.ontrack = (event) => {
        document.getElementById("mortStream").srcObject = event.streams[0];
        document.getElementById("mortStream").style.display = "block";
        document.getElementById("streamOffline").style.display = "none";
    };
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "startBroadcast") {
        chromeToGetMediaHandshake();

        return true; // Indicates an async response might be sent later
    }
});

async function chromeToGetMediaHandshake() {
    await startBroadcast()
}

async function startBroadcast() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            console.log("win")
        })
        .catch(error => console.error("Error accessing microphone:", error));
    ws.send({context:"BroadcastReady"})
}