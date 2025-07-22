
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
    messageCache = await chrome.storage.local.get('cache');
    loadFromCache(messageCache)
  }, 500);
}

init()
document.getElementById("hasStream").textContent = ""
if(chrome.storage.local.get("hasRequest") == "request")
{
  document.getElementById("hasStream").textContent = "New request to Listen Together"
  chrome.storage.local.set({hasRequest: "no request"})
}

function loadFromCache(cache) {
  let chatbody = document.getElementById("chatBody")
  for(let i=0;i<messageCache.cache.length;i++)
  {
    let messageWrapper = document.createElement("div")
    messageWrapper.classList.add("chatMessage")
    let chatUN = document.createElement("span")
    chatUN.classList.add("chatUN")
    chatUN.textContent = `${messageCache.cache[i]["username"]}:`
    chatUN.style.color = messageCache.cache[i]["color"]
    let chatMSG = document.createElement("span")
    chatMSG.classList.add("chatMSG")
    chatMSG.textContent = messageCache.cache[i]["message"]
    messageWrapper.appendChild(chatUN)
    messageWrapper.appendChild(chatMSG)
    chatbody.appendChild(messageWrapper)
  }
}

