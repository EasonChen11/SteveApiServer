from flask import Flask, request, jsonify
from flask_cors import CORS  # include CORS
import requests
import os
from functools import wraps

app = Flask(__name__, static_folder='static')
CORS(app)  # allow all source

API_KEY = os.getenv('API_KEY')
DOCKER_NETWORK = os.getenv('DOCKER_APP_NETWORK')
DOCKER_PORT = os.getenv('DOCKER_PORT')

def check_required_env_vars(*required_vars):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            missing = [var for var in required_vars if not os.getenv(var)]
            if missing:
                return jsonify({'error': f'missing: {", ".join(missing)}'}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/api/send-id', methods=['POST'])
@check_required_env_vars('API_KEY', 'DOCKER_APP_NETWORK', 'DOCKER_PORT')
def send_id():
    data = request.json
    id_tag = data.get('idTag')
    if not id_tag:
        return jsonify({'error': 'ID Tag is required'}), 400

    # send post to SteVe API
    try:
        response = requests.post(f'http://{DOCKER_NETWORK}:{DOCKER_PORT}/steve/api/v1/ocppTags', json={'idTag': id_tag}, headers={'Content-Type': 'application/json', 'STEVE-API-KEY': API_KEY})
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
    pass
