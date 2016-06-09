#!flask/bin/python

TREX_STL_EXT_PATH = "external_libs"

from flask import Flask, jsonify
from error_messages import get_error_message
import imp

Trex = imp.load_source('Trex', 'trex_client/stl/trex_stl_lib')

app = Flask(__name__)

config = {
    'api_version': 0.1,
    'debug': True,
    'port': '8080'
}


# Check server status
@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'result': ''
    })


# Get API version
@app.route('/api_version', methods=['GET'])
def api_version():
    return jsonify({
        'status': 'ok',
        'result': config['api_version']
    })


# Start generating traffic
@app.route('/start', methods=['POST'])
def start_trex():
    return jsonify({
        'status': 'ok',
        'result': 'running'
    })


# Stop sending traffic
@app.route('/stop', methods=['POST'])
def stop_trex():
    return 1


# Get TRex status
@app.route('/get_status', methods=['GET'])
def get_status():
    return 1





# Not implemented methods
@app.errorhandler(404)
def not_implemented(e):
    return jsonify({
        'status': 'error',
        'result': get_error_message('not_implemented')
    })



# if __name__ == '__main__':
#     app.run(debug=config['debug'])
