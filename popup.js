document.getElementById('check-btn').addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      const url = tabs[0].url;
      const result = isPhishing(url) ? "Phishing" : "Legitimate";
      document.getElementById('url-status').textContent = `The website is: ${result}`;
    });
  });
  
  // Function to detect phishing (simplified, same as in background.js)
  function isPhishing(url) {
    const urlLength = url.length;
    const numSubdomains = (new URL(url)).hostname.split('.').length - 2;
    const atSign = url.includes('@') ? 1 : 0;
    const queryLength = new URL(url).search.length;
  
    if (urlLength > 100 || numSubdomains > 2 || atSign === 1 || queryLength > 50) {
      return true;
    }
    return false;
  }
  