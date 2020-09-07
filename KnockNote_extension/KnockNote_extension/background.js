// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';


chrome.runtime.onInstalled.addListener(function() {
  

  chrome.browserAction.onClicked.addListener(function(tab) {
    console.log("browserAction click")
    chrome.storage.sync.get(['userid'], function(result) {
      console.log('userid currently is ' + result.userid);
      if(result.userid == null && window.location.pathname != '/sign.html'){
        chrome.tabs.create({"url": "http://knocknote.s3-website.us-east-2.amazonaws.com/sign.html"})
      }
      else{
        var url = "http://knocknote.s3-website.us-east-2.amazonaws.com/index.html?userid=" + result.userid
        chrome.tabs.create({"url": url});
      }
    });
  });

  chrome.runtime.onMessageExternal.addListener(
  function(request, sender, sendResponse) {
    console.log("message received")
    console.log(request)
    console.log(request.userid)
    if(request.message == "end"){
      chrome.browserAction.setIcon({"path":"images/note_gary.png"})
      chrome.contextMenus.remove("sampleContextMenu")
      chrome.storage.sync.set({'userid': null}, function() {
        console.log('The userid is removed ');
      });
    }
    if(request.message == "start"){
      chrome.browserAction.setIcon({"path":"images/note.png"})
      chrome.storage.sync.set({'userid': request.userid}, function() {
        console.log('The userid is set ' + request.userid);
      });
      chrome.contextMenus.create({
        "id": "sampleContextMenu",
        "title": "addNote",
        "contexts": ["selection","image"]
      });
    }
    
  });
});
chrome.contextMenus.onClicked.addListener(function(info, tab){
        console.log("in the addListener")
        console.log(info)
        chrome.storage.sync.get(['userid'], function(result) {
          console.log('Value currently is ' + result.userid);
          var sendMessage = {"userid":result.userid,
                             "pageurl":info.pageUrl,
                             "imgurl":null,
                             "selectedcontent":null,
                             "writecontent":null}
          if(info.mediaType == null){
            // select text
            sendMessage.selectedcontent = info.selectionText
          }
          else{
            //select image
            sendMessage.imgurl = info.srcUrl
          }

          var note=prompt("Please write some note","")
          console.log("note is "+note)
          if (note!=null)//null is cancled
          {
            console.log("write note success")
            sendMessage.writecontent = note
            console.log(sendMessage)
            var wholeNote = JSON. stringify(sendMessage)
            var addurl = "https://1tlk1ig1cc.execute-api.us-east-2.amazonaws.com/stageone/note"
            var xhr = new XMLHttpRequest();
            xhr.open("PUT", addurl, true);
            xhr.onreadystatechange = function() {
              if (xhr.readyState == 4) {
                var response = JSON.parse(xhr.responseText)
                alert(response.body.content)
              }
            }
            xhr.send(wholeNote);
          }
        });
        

      })

