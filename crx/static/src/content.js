ws = new WebSocket("wss://yt-rpc.onrender.com")

ws.onopen = () => {
    console.log("YT-RPC: Connected to Websocket")
};

ws.onclose = () => {
   
};

let globalPeer
let videoStreamGlobal

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

ws.onmessage = async function (event) {
    const messageData = JSON.parse(event.data);
    switch (messageData["context"]) {

        case "viewerOfferServer":
            viewerOfferServer(messageData);
        break;

        case "iceToStreamerServer":
            globalPeer.addIceCandidate(new RTCIceCandidate(JSON.parse(messageData["candidate"])));
        break;
    }
};

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
function sendMessage(message) {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(message));
        return
    } 
    console.error("YT-RPC: Websocket not open")
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "startBroadcast") {
        chromeToGetMediaHandshake()
    }
    return false;
});

async function chromeToGetMediaHandshake() {
    await startBroadcast()
}

async function startBroadcast() {
    videoStreamGlobal = await navigator.mediaDevices.getDisplayMedia({ audio: true,selfBrowserSurface: "include", })

    ws.send(JSON.stringify({context:"BroadcastReady"}))
}