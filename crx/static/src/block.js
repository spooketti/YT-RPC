//credit to: https://github.com/Michaelunkai/study2/tree/main/Browsers/extensions/Youtube-AdBlocker
//just simplified a lot of it to work for what i need

let isAdFound = false;
let adLoop = 0;

removeAds();

function removeAds() {
    let videoPlayback = 1;

    setInterval(() => {
        let video = document.querySelector('video');
        let ad = document.querySelector('.ad-showing');

        if (ad) {
            isAdFound = true;
            adLoop++;

            if (adLoop < 10) {
                document.querySelector('.ytp-ad-button-icon')?.click();
                document.querySelector('[label="Block ad"]')?.click();
                document.querySelector('.Eddif [label="CONTINUE"] button')?.click();
                document.querySelector('.zBmRhe-Bz112c')?.click();
            } else {
                video?.play();
            }

            let popupContainer = document.querySelector('body > ytd-app > ytd-popup-container > tp-yt-paper-dialog');
            if (popupContainer?.style.display === "") popupContainer.style.display = 'none';

            let skipButtons = [
                '.ytp-ad-skip-button-container', '.ytp-ad-skip-button-modern',
                '.videoAdUiSkipButton', '.ytp-ad-skip-button',
                '.ytp-ad-skip-button-slot'
            ];

            if (video) {
                video.playbackRate = 10;
                video.volume = 0;
                skipButtons.forEach(selector => document.querySelectorAll(selector).forEach(el => el.click()));
                video.currentTime = video.duration + (Math.random() * 0.4 + 0.1) || 0;
            }
        } else {
            if (video?.playbackRate === 10) video.playbackRate = videoPlayback;

            if (isAdFound) {
                isAdFound = false;
                if (videoPlayback === 10) videoPlayback = 1;
                if (video && isFinite(videoPlayback)) video.playbackRate = videoPlayback;
                adLoop = 0;
            } else {
                if (video) videoPlayback = video.playbackRate;
            }
        }
        try {
            document.querySelectorAll("yt-about-this-ad-renderer")[0].parentElement.parentElement.remove()
        }
        catch {
            //honestly nothing cause i prefer not to flood the console legit only reason i wrote this
        }

    }, 50);
}

// function findElementWithText(root, texts) {
//     const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
//         acceptNode: (node) => texts.includes(node.nodeValue.trim()) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP
//     });

//     const textNode = walker.nextNode();
//     return textNode ? textNode.parentElement : null;
// }