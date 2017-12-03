function getCurrentTabTitle(callback) {

    var queryInfo = {
        active: true,
        currentWindow: true
    };

    chrome.tabs.query(queryInfo, function(tabs) {
        var tab = tabs[0];
        var title = tab.title;
        var id = tab.id;
        var url = tab.url;
        callback(title, id, url);
    });
}


function getLastUpdated(id, callback){
    chrome.tabs.sendMessage(id, {"action": "updated"}, function(updated) {
        callback(updated);
    });
}


function sendContent(id, title, updated, url){
    // chrome.tabs.sendMessage(id, {"action": "source"}, function(source) {
    //     $.post("https://1d242726.ngrok.io", {
    //         "content": source,
    //         "title": title,
    //         "updated": updated
    //     }).done(function(data) {
    //         if(data.status !== "error"){
    //             console.log('sending...');
    //
    //
    //
    //             // chrome.tabs.create({'url': "https://1d242726.ngrok.io?title="+title+"&updated="+updated});
    //             // chrome.tabs.sendMessage(id, {"action": "final", "data": data});
    //         } else {
    //             console.log("error");
    //         }
    //         $("#analyze").removeClass('is-loading');
    //     });
    //
    // });

    chrome.tabs.create({'url': "https://1d242726.ngrok.io?title="+title+"&updated="+updated+"&url="+url});


}


document.addEventListener('DOMContentLoaded', function () {
    getCurrentTabTitle(function(title, id, url) {
        getLastUpdated(id, function(updated) {
            document.getElementById('title').innerHTML = title;
            document.getElementById('updated').innerHTML = updated;
            $("#analyze").click(function () {
                $("#analyze").addClass('is-loading');
                sendContent(id, title, updated, url);
            })
        });
    });
});