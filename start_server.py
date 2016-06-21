import sys
import os
from gevent.wsgi import WSGIServer
from app import app

server_config = {
    'port': 5000
}


# Web server function
def main():
    print 'Starting TRex HTTP proxy on port: ', server_config['port']
    http_server = WSGIServer(('', server_config['port']), app)
    http_server.serve_forever()


# Start web server
if __name__ == '__main__':
    try:
        main()
    # Custom message on Exit
    except KeyboardInterrupt:
        print 'TRex HTTP proxy stopped.'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
