document.getElementById("streamMusic").addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (tab) {
    chrome.tabs.sendMessage(tab.id, { action: "startBroadcast" });
  }
});
async function init() {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.tabs.sendMessage(tab.id, { action: "popupOpen" });
}
setTimeout(() => {
  init()  
}, 500);


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
   console.log('hard knock life')
  if (message.type === "loadFromCache") {
    loadFromCache()
  }
});


function loadFromCache() {
  alert("im mentally disabled")
}