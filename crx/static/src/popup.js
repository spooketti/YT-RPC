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

init()

function loadFromCache() {
  
}