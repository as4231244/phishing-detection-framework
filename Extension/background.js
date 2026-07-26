// background.js (Final Stable Server-Based Version)

async function handleTabUpdate(tabId, changeInfo, tab) {
    if (changeInfo.status !== 'complete' || !tab.url || !tab.url.startsWith('http')) {
        return;
    }

    try {
        const sessionData = await chrome.storage.session.get(['whitelistedUrl']);
        if (sessionData.whitelistedUrl === tab.url) {
            await chrome.storage.session.remove('whitelistedUrl');
            return;
        }

        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: tab.url }),
        });

        if (!response.ok) {
            console.error(`Prediction server error: ${response.status}`);
            return;
        }

        const data = await response.json();
        
        const storageData = await chrome.storage.local.get(['safeCount', 'phishingCount', 'lastReset', 'lifetimeTotal']);
        const today = new Date().toISOString().split('T')[0];
        
        let daily = { safe: storageData.safeCount || 0, phishing: storageData.phishingCount || 0 };
        let lifetime = storageData.lifetimeTotal || 0;

        if (storageData.lastReset !== today) {
            daily = { safe: 0, phishing: 0 };
        }

        lifetime++;

        if (data.result === 'PHISHING') {
            daily.phishing++;
            const encodedUrl = encodeURIComponent(tab.url);
            await chrome.tabs.update(tabId, { url: `warning.html?url=${encodedUrl}` });
        } else {
            daily.safe++;
        }

        await chrome.storage.local.set({
            safeCount: daily.safe,
            phishingCount: daily.phishing,
            lifetimeTotal: lifetime,
            lastReset: today
        });

    } catch (e) {
        console.error("Phishing Detector background error:", e);
    }
}

chrome.tabs.onUpdated.addListener(handleTabUpdate);