from flask import Flask, render_template, request, Response
from utils.extractor import get_data
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/api", methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        return 'GET'
    elif request.method == 'POST':
        try:
            schema_name = request.form['schemas']
            message = get_data(schema_name)
        except:
            message = {"status": "error",
                       "message": 'Error'}
        payload = json.dumps(message)
        return Response(payload, status=201, mimetype='application/json')


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=3333)
