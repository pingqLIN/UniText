console.log("Content script starter loaded");

void chrome.runtime
  .sendMessage({ type: "PING" })
  .then((response) => console.log("Background response", response))
  .catch(() => {
    console.log("Content script is not wired into manifest.json yet");
  });
