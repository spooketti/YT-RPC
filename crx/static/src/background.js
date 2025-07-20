chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse){
      if(request.type === "loadFromCache")
      {
          chrome.storage.local.set({ cache: request.message });
      }
    }
);