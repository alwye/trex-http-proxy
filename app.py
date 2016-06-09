#!flask/bin/python
from flask import Flask, jsonify
from error_messages import get_error_message
import t_rex_stateless as Trex
import thread
from cors_decorator import crossdomain

app = Flask(__name__)

config = {
    'api_version': 0.1,
    'is_running': False
}


def start_traffic(threadName, delay):

    print threadName, delay

    traffic_config = {
        'duration': 20,
        'rate': '10000pps',
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
    return jsonify({
        'status': 'ok',
        'result': 'ok'
    })


# Get API version
@app.route('/api_version', methods=['GET'])
@crossdomain(origin='*')
def api_version():
    return jsonify({
        'status': 'ok',
        'result': config['api_version']
    })


# Start generating traffic
@app.route('/start', methods=['POST'])
@crossdomain(origin='*')
def start_trex(args):

    print

    if not config['is_running']:
        config['is_running']= True
        thread.start_new_thread(start_traffic, ("Thread-1", 2,))
    else:
        stop_trex()
        start_trex(args)

    return jsonify({
        'status': 'ok',
        'result': 'start'
    })


# Stop sending traffic
@app.route('/stop', methods=['POST'])
@crossdomain(origin='*')
def stop_trex():
    config['is_running'] = False
    Trex.stop_client()
    return jsonify({
        'status': 'ok',
        'result': 'stop'
    })


# Get TRex status
@app.route('/get_status', methods=['GET'])
@crossdomain(origin='*')
def get_status():
    return jsonify({
        'status': 'ok',
        'result': "running" if config['is_running'] else "stopped"
    })


# Not implemented methods
@app.errorhandler(404)
def not_implemented(e):
    return jsonify({
        'status': 'error',
        'result': get_error_message('not_implemented')
    }), 404
