from flask import Flask, render_template, request, Response
from utils.extractor import fetch_data, extract_columns, filter_data, enrich_data, transform_to_json
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
            dataset_json = fetch_data('2022-05-01','NOW')
            dataset_df = extract_columns(dataset_json)
            filtered_df = filter_data(dataset_df)
            enriched_data = enrich_data(filtered_df)
            final_json = transform_to_json(enriched_data)

        except:
            final_json = {"status": "error",
                       "message": 'Error'}
        payload = json.dumps(final_json)
        return Response(payload, status=201, mimetype='application/json')


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=3333)
