#!flask/bin/python
from flask import Flask, jsonify, request
from error_messages import get_error_message
# import t_rex_stateless as Trex
import trex_api as Trex
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

    default_traffic_config = {
        'duration': -1,  # -1 for infinity
    }

    Trex.start_traffic(
        duration=default_traffic_config['duration'],
        pkts_n=traffic_config['pkts_n'],
        pps=traffic_config['pps'],
        mac_dest=traffic_config['mac_dest'],
        src_n=traffic_config['src_n']
    )

    return 0


# Check server status
@app.route('/', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'OPTIONS'])
def index():
    return responsify('ok', 'ok')


# Get API version
@app.route('/api_version', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'OPTIONS'])
def api_version():
    return responsify('ok', config['api_version'])


# Start generating traffic
@app.route('/start', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', methods=['POST', 'OPTIONS'])
def start_trex():
    if request.method == 'POST':
        if request.is_json:
            req_data = request.get_json(cache=False)
            if req_data is not None:
                try:
                    traffic_config = {
                        "pps": int(req_data['input']['pps'].encode("ascii")),
                        "src_n": int(req_data['input']['src_n'].encode("ascii")),
                        "pkts_n": int(req_data['input']['pkts_n'].encode("ascii")),
                        "mac_dest": req_data['input']['mac_dest'].encode("ascii")
                    }
                    if traffic_config["pps"] > 0 and traffic_config["mac_dest"]:
                        if not Trex.is_running():
                            try:
                                thread.start_new_thread(start_traffic, (traffic_config,))
                            except:
                                return responsify('error', get_error_message('trex_not_start'))
                            return responsify('ok', 'start')
                        else:
                            return responsify('error', get_error_message('trex_already_running'))
                    else:
                        return responsify('error', get_error_message('negative_pps'))

                except (AttributeError, KeyError):
                    return responsify('error', get_error_message('not_json'))
                except ValueError:
                    return responsify('error', get_error_message('ascii_error'))
            else:
                return responsify('error', get_error_message('not_json'))
        else:
            return responsify('error', get_error_message('not_json'))
    else:
        return responsify("ok", "ok")


# Stop sending traffic
@app.route('/stop', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', methods=['POST', 'OPTIONS'])
def stop_trex():
    if request.method == 'POST':
        Trex.stop_traffic()
        return responsify('ok', 'stop')
    else:
        return responsify("ok", "ok")


# Get TRex traffic status
@app.route('/get_status', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'OPTIONS'])
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
