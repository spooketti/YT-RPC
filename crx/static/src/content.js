ws = new WebSocket("wss://yt-rpc.onrender.com")
let popupPort = null;

chrome.runtime.onConnect.addListener((port) => {
  if (port.name === "YT-RPC-chatport") {
    popupPort = port;
  }
});

function sendToPopup() {
  if (popupPort) {
    popupPort.postMessage({ payload: "chat" });
  }
}

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
    answer.sdp = answer.sdp.replace(
  'useinbandfec=1',
  'useinbandfec=1; stereo=1; maxaveragebitrate=510000'
);
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
    videoStreamGlobal = await navigator.mediaDevices.getDisplayMedia({video:true, audio: {
        autoGainControl: false,
        channelCount: 2,
        echoCancellation: false,
        latency: 0,
        noiseSuppression: false,
        sampleRate: 48000,
        sampleSize: 16,
        volume: 1.0
      },selfBrowserSurface: "include", })

    ws.send(JSON.stringify({context:"BroadcastReady"}))
}

let fontInject = document.createElement("link")
fontInject.rel = "stylesheet"
fontInject.href = "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"
document.head.appendChild(fontInject)

const sheet = document.styleSheets[0];
sheet.insertRule('#rpcNotif:hover { filter:opacity(0); }', sheet.cssRules.length);

let ltNotif = document.createElement("div")
ltNotif.style.position = "fixed"
ltNotif.style.top = 0
ltNotif.style.right = 0
ltNotif.textContent = "YT-RPC Listen Together Notifications"
ltNotif.style.backgroundColor = "white"
ltNotif.style.display = "flex"
ltNotif.style.alignItems = "center"
ltNotif.style.color = "black"
ltNotif.style.zIndex = "999"
ltNotif.style.transition = "all 0.25s"
ltNotif.id = "rpcNotif"
ltNotif.style.userSelect = "none"
document.body.appendChild(ltNotif)

let bellIcon = document.createElement("span")
bellIcon.id = "rpcBellIcon"
bellIcon.classList.add("material-symbols-outlined")
bellIcon.innerText = "notifications"
ltNotif.appendChild(bellIcon)