let rpcFrame = document.getElementById("rpcFrame")

document.getElementById("streamMusic").addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (tab) {
    chrome.tabs.sendMessage(tab.id, { action: "startBroadcast" });
  }
});
async function init() {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.tabs.sendMessage(tab.id, { action: "popupOpen" });
  setTimeout(async () => {
    messagecache = await chrome.storage.local.get('cache');
    console.log(messageCache)
  }, 500);
}


chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.msg === "BGnewMSG") {
           loadFromCache(data)
        }
    }
);

init()

function loadFromCache(data) {
   rpcFrame.contentWindow.postMessage({ action: "loadCache", cache:data});
}