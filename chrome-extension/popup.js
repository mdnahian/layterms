function getCurrentTabTitle(callback) {

    var queryInfo = {
        active: true,
        currentWindow: true
    };

    chrome.tabs.query(queryInfo, function(tabs) {
        var tab = tabs[0];
        var title = tab.title;
        var id = tab.id;
        callback(title, id);
    });
}


function getLastUpdated(callback){
    callback(document.lastModified.substring(0, 10));
}


function sendContent(id, title, updated){
    $.post("https://1d242726.ngrok.io/api/content", {
        "content": "",
        "title": title,
        "updated": updated
    }).done(function(data) {
        console.log(data);
        var response = JSON.parse(data);
        if(response.error == null){
            chrome.tabs.sendMessage(id, {"data": response});
        } else {
            console.log(response.message);
        }
    });
}


document.addEventListener('DOMContentLoaded', function () {
    getCurrentTabTitle(function(title, id) {
        getLastUpdated(function(updated) {
            document.getElementById('title').innerHTML = title;
            document.getElementById('updated').innerHTML = updated;
            $("#analyze").click(function () {
                sendContent(id, title, updated);
            })
        });
    });
});