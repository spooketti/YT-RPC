chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "startBroadcast") {
        chromeToGetMediaHandshake();

        return true; // Indicates an async response might be sent later
    }
});

async function chromeToGetMediaHandshake() {
    await getMedia()
}

async function getMedia() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            console.log("win")
        })
        .catch(error => console.error("Error accessing microphone:", error));

}