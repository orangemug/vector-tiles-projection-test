import json
import glob
import logging
from flask import Flask, send_from_directory, render_template, make_response
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
logging.basicConfig(level=logging.DEBUG)

def localify(v):
    return v.replace(
        "https://orangemug.github.io/vector-tile-projection-test",
        "http://localhost:5007"
    )

@app.route('/styles/')
def list_style():
    files = glob.glob("styles/*.json")
    return render_template('styles.html', files=files)

@app.route('/styles/<path>')
def send_style(path):
    style_path = 'styles/{0}'.format(path)
    app.logger.info('loading %s', style_path)
    with open(style_path) as json_file:
        data = json.load(json_file)
        sources = data.get('sources')
        for key in sources:
            source = sources.get(key)
            tiles = source.get('tiles')
            tiles = list(map(localify, tiles))
            source['tiles'] = tiles

        r = make_response(
            json.dumps(data, indent=2)
        )
        r.mimetype = 'application/json'
        return r

@app.route('/vectortiles/<path:path>')
def send_vt(path):
    return send_from_directory('vectortiles', path)

if __name__ == "__main__":
    handler = app.run(port=5007, host="0.0.0.0")

