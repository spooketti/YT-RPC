let latestData = null;
let popupPort = null;

chrome.runtime.onConnect.addListener((port) => {
  if (port.name === "popup") {
    popupPort = port;

    port.onDisconnect.addListener(() => {
      popupPort = null;
    });

    if (latestData) {
      popupPort.postMessage({ type: "cachedData", data: latestData });
    }
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "dataFromContent") {
    latestData = message.data;
    // Forward to popup if connected
    if (popupPort) {
      popupPort.postMessage({ type: "newData", data: latestData });
    }
  }
});
