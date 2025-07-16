document.getElementById("streamMusic").addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (tab) {
        chrome.tabs.sendMessage(tab.id, { action: "startBroadcast" });
    }
});

let a = 0
a++
document.getElementById("a").textContent = a

const port = chrome.runtime.connect({ name: "YT-RPC-chatport" });
port.onMessage.addListener((msg) => {
  document.getElementById("a").textContent = msg.payload;
});