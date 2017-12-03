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


function getLastUpdated(id, callback){
    chrome.tabs.sendMessage(id, {"action": "updated"}, function(updated) {
        callback(updated);
    });
}


function sendContent(id, title, updated){
    chrome.tabs.sendMessage(id, {"action": "source"}, function(source) {
        $.post("https://1d242726.ngrok.io/api/content", {
            "content": source,
            "title": title,
            "updated": updated
        }).done(function(data) {
            if(data.status !== "error"){
                console.log('sending...');
                chrome.tabs.create({'url': chrome.extension.getURL('response.html')+"?title="+title+"&updated="+updated});
                // chrome.tabs.sendMessage(id, {"action": "final", "data": data});
            } else {
                console.log("error");
            }
            $("#analyze").removeClass('is-loading');
        });

    });


}


document.addEventListener('DOMContentLoaded', function () {
    getCurrentTabTitle(function(title, id) {
        getLastUpdated(id, function(updated) {
            document.getElementById('title').innerHTML = title;
            document.getElementById('updated').innerHTML = updated;
            $("#analyze").click(function () {
                $("#analyze").addClass('is-loading');
                sendContent(id, title, updated);
            })
        });
    });
});