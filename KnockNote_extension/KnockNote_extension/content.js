// alert("Hello from your Chrome extension!")
// alert(window.location.hostname)
chrome.storage.sync.get(['userid'], function(result) {
  console.log('userid currently is ' + result.userid);
  if(result.userid == null && window.location.pathname != '/sign.html'){
    window.location.replace("http://knocknote.s3-website.us-east-2.amazonaws.com/sign.html")
  }
});
