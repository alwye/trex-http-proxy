#!flask/bin/python
from flask import Flask, jsonify, request
from error_messages import get_error_message
import t_rex_stateless as Trex
import thread
from cors_decorator import crossdomain

app = Flask(__name__)

config = {
    'api_version': 0.1,
    'is_running': False
}


def responsify(status, result):
    return jsonify({
        'output': {
            'status': status,
            'result': result
        }
    })


def start_traffic(pps):

    traffic_config = {
        'duration': 20,
        'rate': pps + 'pps',
        'warmup_time': 0,
        'async_start': False
    }

    traffic_options = {'p1_src_start_ip': '10.10.10.2', 'p2_src_start_ip': '20.20.20.2', 'p2_dst_start_ip': '10.10.10.2',
     'p2_src_end_ip': '20.20.20.254', 'p1_src_end_ip': '10.10.10.254', 'p1_dst_start_ip': '20.20.20.2'}

    pkt_a, pkt_b = Trex.create_packets(traffic_options, 1500)

    Trex.simple_burst(
        pkt_a, pkt_b, traffic_config['duration'], traffic_config['rate'], traffic_config['warmup_time'], traffic_config['async_start']
    )

    config['is_running'] = False

    return 0


# Check server status
@app.route('/')
@crossdomain(origin='*')
def index():
    return responsify('ok', 'ok')


# Get API version
@app.route('/api_version', methods=['GET'])
@crossdomain(origin='*')
def api_version():
    return responsify('ok', config['api_version'])


@app.route('/test', methods=['POST'])
@crossdomain(origin='*')
def http_test():
    if request.is_json:
        print request.get_json()
        return responsify('ok', 'test')
    return responsify('error', get_error_message('not_json'))


# Start generating traffic
@app.route('/start', methods=['POST'])
@crossdomain(origin='*')
def start_trex():
    req_data = request.get_json

    if req_data is not None:
        try:
            pps = req_data['traffic_config']['pps']
            if not config['is_running']:
                config['is_running'] = True
                try:
                    thread.start_new_thread(start_traffic, pps)
                except:
                    return responsify('error', get_error_message('trex_not_start'))
            else:
                stop_trex()
                start_trex()
            return responsify('ok', 'start')

        except AttributeError:
            return responsify('error', get_error_message('not_json'))

    return responsify('error', get_error_message('not_json'))


# Stop sending traffic
@app.route('/stop', methods=['POST'])
@crossdomain(origin='*')
def stop_trex():
    config['is_running'] = False
    Trex.stop_client()
    return responsify('ok', 'stop')


# Get TRex status
@app.route('/get_status', methods=['GET'])
@crossdomain(origin='*')
def get_status():
    return responsify('ok', "running" if config['is_running'] else "stopped")


# Not implemented methods
@app.errorhandler(404)
def not_implemented(e):
    return responsify('error', get_error_message('not_implemented')), 404
