

var style = '<style>.reacts-container { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgb(0, 0, 0); background: rgba(0, 0, 0, 0.5); z-index: 9999; overflow:hidden; overflow-y:auto; } .reacts-modal { position: absolute; width: 960px; height:100%; min-height: 640px; background-color: #ffffff; padding: 16px; left: 50%; top:0; bottom:0; margin-left: -480px; } .close-btn { position: absolute; right: 16px; top: 16px; color: #242424; font-weight: bold; font-family: Verdana; cursor: pointer; font-size:36px; } .reacts-modal-content { margin-top:16px; } .reacts-list-active { display: block; } .reacts-modal-title h2, .reacts-modal-title h5 { margin-top:0; margin-bottom:0; } .reacts-modal-content table { width:100%; } .reacts-modal-content th { padding:4px; background-color:#eeeeee; } .reacts-modal-content td { padding:4px; }</style>';
var js = '<script>$("#closeBtn").click(function() { $("#reactsModal").toggleClass("reacts-list-active") });</script>';

var loaded = false;

function modal(data){
    data = JSON.parse(data);
    console.log(data.title);
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


// function reloadContent(title, updated, callback) {
//     $.post("https://1d242726.ngrok.io/api/content", {
//         "content": getData(),
//         "title": title,
//         "updated": updated
//     }).done(function(data) {
//         console.log('second time');
//         if(data.status !== "error"){
//             callback(data);
//         } else {
//             console.log("error");
//             callback([]);
//         }
//         $("#analyze").removeClass('is-loading');
//     });
// }


function getData(){
    var html_text = document.getElementsByTagName('body')[0].innerHTML.replace(/<[^>]+>/g, '');
    return he.decode(html_text)
}






document.addEventListener('DOMContentLoaded', function () {
    var url = new URL(window.location.href);
    var title = url.searchParams.get("title");
    var updated = url.searchParams.get("updated");


    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(data) {
        if (this.readyState == 4 && this.status == 200) {
            if(!loaded){

                document.getElementsByTagName('head')[0].innerHTML = document.getElementsByTagName('head')[0].innerHTML + style;
                document.getElementsByTagName("body")[0].innerHTML = modal(data.currentTarget.responseText) + js + document.getElementsByTagName('body')[0].innerHTML;

                loaded = true;
            }

            $("#reactsModal").toggleClass('reacts-list-active');
        }
    };
    xhttp.open("POST", "https://1d242726.ngrok.io/api/summary", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("title="+title+"&updated="+updated+"&content="+getData());


    // var data = {"status": "success", "updated": "hello", "modal": [{"content": "\n mdni007\nTwitter Privacy Policy\n\nOur Services instantly connect people everywhere to what\u2019s most meaningful to them. For example, any registered user of Twitter can send a Tweet, which is public by default, and can include a message of 140 characters or less and content like photos, videos, and links to other websites. This Privacy Policy describes how and when we collect, use, and share your information across our websites, SMS, APIs, email notifications, applications, buttons, embeds, ads, and our other covered services that link to this Policy (collectively, the \u201cServices\u201d), and from our partners and other third parties.", "type": "text", "title": "Summary"}, {"content": {"headers": ["Type of Data", "Collected?*", "Context"], "rows": [["Microphone", false, "-"], ["Accelerometer", false, "-"], ["Contacts", false, "-"], ["Site you came from", false, "-"], ["IP address", false, "-"], ["Camera", false, "-"], ["Web beacons", false, "-"], ["Email address", false, "-"], ["Phone number", false, "-"], ["Photos", false, "-"], ["Gyroscope", false, "-"], ["Address", false, "-"], ["Device", false, "-"], ["Browser", false, "-"], ["Operating system", false, "-"], ["Name", false, "-"], ["Gender", false, "-"], ["Birthdate", false, "-"], ["Payment information", false, "-"], ["GPS", false, "-"], ["Cookies", false, "-"], ["SSN", false, "-"]]}, "type": "table", "title": "Data Collected"}, {"content": {"headers": ["Entity", "Data Shared?", "Context"], "rows": [["Authorities", false, "-"], ["Advertisers", false, "-"], ["Service providers", false, "-"], ["Corporate affiliates", false, "-"]]}, "type": "table", "title": "Who your data is shared with"}], "title": "hi"};
    // document.getElementsByTagName('head')[0].innerHTML = document.getElementsByTagName('head')[0].innerHTML + style;
    // document.getElementsByTagName("body")[0].innerHTML = modal(data) + js + document.getElementsByTagName('body')[0].innerHTML;
    // $("#reactsModal").toggleClass('reacts-list-active');

});
