from flask import Flask, request, url_for, render_template, url_for
import os
import json
import analyze_policy
import summary
import getEntityGraph
import requests
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def content():

    link = request.args.get('url')
    title = request.args.get('title')
    updated= request.args.get('updated')
    html = requests.get(link).text
    soup = BeautifulSoup(html)
    text = ''.join(soup.findAll(text=True))

    sum= ''

    try:
        sum = summary.get_summary(text.encode('utf-8'))
        getEntityGraph.kindamain(text.encode('utf-8'))
    except:
        pass


    info, entity = analyze_policy.analyze(text)

    return render_template('index.html', info=info
, entity=entity, sum=sum, title=title, updated=updated)   # return ''

    #     return json.dumps({
    #         "modal": [
    #             {
    #                 "title": "Summary",
    #                 "content": sum,
    #                 "type": "text"
    #             },
    #             {
    #                 "title": "Data Collected",
    #                 "content": {
    #                     "headers": [
    #                         "Type of Data",
    #                         "Collected?*",
    #                         "Context"
    #                     ],
    #                    [['Microphone', False, '-'], ['Accelerometer', False, '-'], ['Contacts', False, '-'], ['Site you came from', False, '-'], ['IP address', False, '-'], ['Camera', False, '-'], ['Web beacons', False, '-'], ['Email address', False, '-'], ['Phone number', False, '-'], ['Photos', False, '-'], ['Gyroscope', False, '-'], ['Address', False, '-'], ['Device', False, '-'], ['Browser', False, '-'], ['Operating system', False, '-'], ['Name', False, '-'], ['Gender', False, '-'], ['Birthdate', False, '-'], ['Payment information', False, '-'], ['GPS', False, '-'], ['Cookies', False, '-'], ['SSN', False, '-']]
    #                 },
    #                 "type": "table"
    #             },
    #             {
    #                 "title": "Who your data is shared with",
    #                 "content": {
    #                     "headers": [
    #                         "Entity",
    #                         "Data Shared?",
    #                         "Context"
    #                     ],
    #                     "rows": [['Authorities', False, '-'], ['Advertisers', False, '-'], ['Service providers', False, '-'], ['Corporate affiliates', False, '-']]
    #                 },
    #                 "type": "table"
    #             }
    #         ],
    #         "title": title,
    #         "updated": updated,
    #         "status": "success"
    #     })
    # return '{"status": "error", "message": "invalid request method"}'



@app.route('/api/summary', methods=['POST'])
def sumry():
    if request.method == 'POST':
        text = request.form['content']
        title = request.form['title']
        updated = request.form['updated']

        sum = summary.get_summary(text)
        return json.dumps({
            "modal": [
                {
                    "title": "Summary",
                    "content": sum,
                    "type": "text"
                }
            ],
            "title": title,
            "updated": updated,
            "status": "success"
        })
    return '{"status": "error", "message": "invalid request method"}'





def filter(arr):
    brr = []
    for ar in arr:
        br = []
        for a in ar:
            if a == None:
                br.append("-")
            else:
                br.append(a)
        brr.append(br)
    return brr




@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)