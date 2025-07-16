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