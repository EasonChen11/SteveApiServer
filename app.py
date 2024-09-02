from flask import Flask, request, jsonify
from flask_cors import CORS  # include CORS
import requests

app = Flask(__name__, static_folder='static')
CORS(app)  # allow all source

@app.route('/send-id', methods=['POST'])
def send_id():
    data = request.json
    id_tag = data.get('idTag')

    if not id_tag:
        return jsonify({'error': 'ID Tag is required'}), 400

    # send post to SteVe API
    try:
        response = requests.post('http://steve-steve-360-app-1:8180/steve/api/v1/ocppTags', json={'idTag': id_tag}, headers={'Content-Type': 'application/json', 'STEVE-API-KEY': 'a'})
        # http://127.0.0.1:8180/steve/api/v1/ocppTags
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to get a valid response from SteVe API', 'status_code': response.status_code}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
