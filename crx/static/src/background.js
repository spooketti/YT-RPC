chrome.runtime.onMessage.addListener(
  function (request, sender, sendResponse) {
    if (request.type === "loadFromCache") {
      chrome.storage.local.set({ cache: request.message });
    }
    // if (request.type === "newMSG") {
    //   chrome.runtime.sendMessage({
    //     msg: "BGnewMSG",
    //     data: request.message
    //   });
    // }
    if(request.type === "streamRequest")
    {
      chrome.storage.local.set({watchrequest: "request"})
    }
  }
);