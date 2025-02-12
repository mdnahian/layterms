
var style = '<style>.reacts-container { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgb(0, 0, 0); background: rgba(0, 0, 0, 0.5); z-index: 9999; overflow:hidden; overflow-y:auto; } .reacts-modal { position: absolute; width: 960px; height:100%; min-height: 640px; background-color: #ffffff; padding: 16px; left: 50%; top:0; bottom:0; margin-left: -480px; } .close-btn { position: absolute; right: 16px; top: 16px; color: #242424; font-weight: bold; font-family: Verdana; cursor: pointer; font-size:36px; } .reacts-modal-content { margin-top:16px; } .reacts-list-active { display: block; } .reacts-modal-title h2, .reacts-modal-title h5 { margin-top:0; margin-bottom:0; } .reacts-modal-content table { width:100%; } .reacts-modal-content th { padding:4px; background-color:#eeeeee; } .reacts-modal-content td { padding:4px; }</style>';
var js = '<script>$("#closeBtn").click(function() { $("#reactsModal").toggleClass("reacts-list-active") });</script>';

var loaded = false;

function modal(data){
    data = JSON.parse(data);
    return '<div id="reactsModal" class="reacts-container"> ' +
                '<div id="closeBtn" class="close-btn">X</div> ' +
                '<div class="reacts-modal"> ' +
                    '<div class="reacts-modal-title"> ' +
                        '<h2>'+data.title+'</h2> ' +
                        '<h5>'+data.updated+'</h3> ' +
                    '</div> ' +
                    generateContent(data) +
                '</div> ' +
             '</div>';
}



function generateContent(data) {
    var content = "";
    var modal = data.modal;
    for(var i=0; i<modal.length; i++){
        if(modal[i].type === "text"){
            content += '<div class="reacts-modal-content"><h3>'+modal[i].title+'</h3> <p>'+modal[i].content+'</p> </div>';
        } else if(modal[i].type === "table"){
            var headers = "<th>";
            for(var j=0; j=modal[i].content.headers.length; j++){
                headers += '<th>'+modal[i].content.headers[j]+'</th>';
            }
            headers += "</th>";
            var rows = '';
            for(var k=0; k<modal[i].content.rows.length; k++){
                rows += '<tr>';
                for(var l=0; l<modal[i].content.rows[k]; l++) {
                    rows += '<td>'+modal[i].content.rows[k][l]+'</td>';
                }
                rows += '</tr>';
            }
            content += '<div class="reacts-modal-content">' +
                    '<h3>'+modal[i].title+'</h3>' +
                    '<table>' +
                        '<thead>' +
                           headers +
                        '</thead>' +
                        '<tbody>' +
                            rows +
                        '</tbody>' +
                    '</table>' +
                '</div>';
        } else if(modal[i].type === "list"){
            var list = "";
            for(var m=0; m<modal[i].content.length; m++){
                list += "<li>"+modal[i].content[m]+"</li>";
            }
            content += '<div class="reacts-modal-content">' +
                    '<ol>' +
                        list +
                    '</ol>' +
                '</div>';
        }
    }
    return content;
}


function reloadContent(title, updated, callback) {
    $.post("https://1d242726.ngrok.io/api/content", {
        "content": getData(),
        "title": title,
        "updated": updated
    }).done(function(data) {
        console.log('second time');
        if(data.status !== "error"){
            callback(data);
        } else {
            console.log("error");
            callback([]);
        }
        $("#analyze").removeClass('is-loading');
    });
}


function getData(){
    var html_text = document.getElementsByTagName('body')[0].innerHTML.replace(/<[^>]+>/g, '');
    return he.decode(html_text)
}



chrome.runtime.onMessage.addListener(
    function(request, sender, callback) {
        console.log('done');
        if(request.action === 'source'){
            callback(getData());
        } else if(request.action === "final") {

            reloadContent(request.data.title, request.data.updated, function (data) {
                if(!loaded){
                    document.getElementsByTagName('head')[0].innerHTML = document.getElementsByTagName('head')[0].innerHTML + style;
                    document.getElementsByTagName("body")[0].innerHTML = modal(data) + js + document.getElementsByTagName('body')[0].innerHTML;

                    loaded = true;
                }

                $("#reactsModal").toggleClass('reacts-list-active');
            });

        } else if(request.action === "updated"){
            callback(document.lastModified.substring(0, 10));
        } else {
            console.log(request)
        }
    }
);




