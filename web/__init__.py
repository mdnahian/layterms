from flask import Flask, request, url_for
import os

app = Flask(__name__)


@app.route('/')
def index():
    return 'running...'


@app.route('/api/content', methods=['POST'])
def content():
    if request.method == 'POST':
        print request.form
        text = request.form['content']
        title = request.form['title']
        updated = request.form['updated']

        

    return ''



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