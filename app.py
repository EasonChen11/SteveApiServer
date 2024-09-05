from flask import Flask, request, jsonify
from flask_cors import CORS  # include CORS
import requests
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # allow all source

@app.route('/api/send-id', methods=['POST'])
def send_id():
    data = request.json
    id_tag = data.get('idTag')
    API_KEY = os.getenv('API_KEY')
    DOCKER_NETWORK = os.getenv('DOCKER_NETWORK', 'steve-steve-360-app-1')
    DOCKER_PORT = os.getenv('DOCKER_PORT', 8180)
    print(DOCKER_NETWORK, DOCKER_PORT)
    if not API_KEY:
        return jsonify({'error': 'API Key is required'}), 400
    if not id_tag:
        return jsonify({'error': 'ID Tag is required'}), 400

    # send post to SteVe API
    try:
        response = requests.post(f'http://{DOCKER_NETWORK}:{DOCKER_PORT}/steve/api/v1/ocppTags', json={'idTag': id_tag}, headers={'Content-Type': 'application/json', 'STEVE-API-KEY': API_KEY})
        # response = requests.post('http://steve-steve-360-app-1:8180/steve/api/v1/ocppTags', json={'idTag': id_tag}, headers={'Content-Type': 'application/json', 'STEVE-API-KEY': 'a'})
        # http://127.0.0.1:8180/steve/api/v1/ocppTags
        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 201:
            return jsonify({'success':f'add the idTag ={id_tag} authorized'})
        elif response.status_code == 422:
            return jsonify({'fail':f'the idTag ={id_tag} is exist'})
        else:
            return jsonify({'error': 'Failed to get a valid response from SteVe API', 'status_code': response.status_code}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
# more api ... @app.route('/api/...', methods=['POST'])
if __name__ == '__main__':
    # FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT')
    # FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST')
    # app.run(debug=True, host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
    pass
