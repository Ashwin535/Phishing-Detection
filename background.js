function isPhishing(url) {
    const urlLength = url.length;
    const numSubdomains = (new URL(url)).hostname.split('.').length - 2;
    const atSign = url.includes('@') ? 1 : 0;
    const queryLength = new URL(url).search.length;
  
    // Simple heuristic-based rule (you can replace this with a more complex ML model)
    if (urlLength > 100 || numSubdomains > 2 || atSign === 1 || queryLength > 50) {
      return true;
    }
    return false;
  }
  
  // Listen to active tab updates and check for phishing
  chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (changeInfo.status === 'complete') {
      const url = tab.url;
      if (isPhishing(url)) {
        chrome.browserAction.setIcon({path: "icons/phishing-icon-48.png"});
        chrome.browserAction.setTitle({title: "Phishing Detected!"});
        chrome.tabs.executeScript(tabId, {
          code: 'alert("This website is potentially a phishing site!");'
        });
      } else {
        chrome.browserAction.setIcon({path: "icons/phishing-icon-16.png"});
        chrome.browserAction.setTitle({title: "Safe Website"});
      }
    }
  });
  