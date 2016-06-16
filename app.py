#!flask/bin/python
from flask import Flask, jsonify, request
from error_messages import get_error_message
import t_rex_stateless as Trex
import thread
from cors_decorator import crossdomain
import pprint

app = Flask(__name__)

config = {
    'api_version': 0.1,
}


def responsify(status, result):
    return jsonify({
        'output': {
            'status': status,
            'result': result
        }
    })


def start_traffic(traffic_config):

    rate = traffic_config['pps'] + "pps"

    default_traffic_config = {
        'duration': -1,
        'warmup_time': 0,
        'async_start': False
    }

    traffic_options = {
        'p1_src_start_ip': '10.10.10.2',
        'p2_src_start_ip': '20.20.20.2',
        'p2_dst_start_ip': '10.10.10.2',
        'p2_src_end_ip': '20.20.20.254',
        'p1_src_end_ip': '10.10.10.254',
        'p1_dst_start_ip': '20.20.20.2'
    }

    pkt_a, pkt_b = Trex.create_packets(traffic_options, traffic_config['mac_dest'], 1500)

    Trex.simple_burst(
        pkt_a=pkt_a,
        pkt_b=pkt_b,
        rate=rate,
        duration=default_traffic_config['duration'],
        warmup_time=default_traffic_config['warmup_time'],
        async_start=default_traffic_config['async_start']
    )

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


# Start generating traffic
@app.route('/start', methods=['POST'])
@crossdomain(origin='*')
def start_trex():
    if request.is_json:
        req_data = request.get_json(cache=False)
        if req_data is not None:
            try:
                traffic_config = {
                    "pps": req_data['input']['pps'].encode("ascii"),
                    "src_n": req_data['input']['src_n'].encode("ascii"),
                    "mac_dest": req_data['input']['mac_dest'].encode("ascii")
                }
                if not Trex.is_running():
                    try:
                        thread.start_new_thread(start_traffic, (traffic_config,))
                    except:
                        return responsify('error', get_error_message('trex_not_start'))
                else:
                    stop_trex()
                    start_trex()
                return responsify('ok', 'start')

            except (AttributeError, KeyError):
                return responsify('error', get_error_message('not_json'))
            except ValueError:
                return responsify('error', get_error_message('ascii_error'))
        else:
            return responsify('error', get_error_message('not_json'))
    else:
        return responsify('error', get_error_message('not_json'))


# Stop sending traffic
@app.route('/stop', methods=['POST'])
@crossdomain(origin='*')
def stop_trex():
    Trex.stop_client()
    return responsify('ok', 'stop')


# Get TRex traffic status
@app.route('/get_status', methods=['GET'])
@crossdomain(origin='*')
def get_status():
    status = Trex.is_running()
    stats = Trex.get_stats()

    return responsify('ok', {
        "status": "running" if status else "stopped",
        "stats": stats
    })


# Not implemented methods
@app.errorhandler(404)
def not_implemented(e):
    return responsify('error', get_error_message('not_implemented')), 404
