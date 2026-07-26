// warning.js (Updated with "Permission Slip" logic)

document.addEventListener('DOMContentLoaded', () => {
  const proceedBtn = document.getElementById('proceedBtn');
  const urlParams = new URLSearchParams(window.location.search);
  const blockedUrlEncoded = urlParams.get('url');
  
  if (blockedUrlEncoded) {
    const blockedUrl = decodeURIComponent(blockedUrlEncoded);

    proceedBtn.addEventListener('click', () => {
      // 1. Create the "permission slip" in Chrome's session storage.
      // This tells the background script which URL to temporarily ignore.
      // We also add a timestamp to make sure the permission expires.
      chrome.storage.session.set({ 'whitelistedUrl': blockedUrl, 'timestamp': Date.now() });

      // 2. Navigate to the original, blocked URL.
      window.location.href = blockedUrl;
    });
  } else {
    // Handle case where the page is loaded without a URL parameter
    proceedBtn.textContent = 'No URL specified';
    proceedBtn.disabled = true;
  }
});