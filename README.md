# TRex HTTP Proxy
## Overview
This HTTP Proxy allows you to integrate TRex traffic generator (https://trex-tgn.cisco.com) into HTTP environment. For example, it is convenient way to manage the TRex instance via web interface.

## Requirements
You need to have Python 2.7 supported.

Run the following command to install required [PyPi](https://pypi.python.org/pypi) packages:

```
pip install -r requirements.txt
```

## Get it running

cd to TRex's scripts folder and run the interactive console like this:

```
sudo ./t-rex-64 -i
```

Once your Python meets the requirements you'll be able to run the proxy with this commands:
 
```
python start_server.py
```

To examine API, look into the [Postman](https://www.getpostman.com) collection: **Postman-APIs.postman_collection**.

## Possible problems
### Trex on Mac
Trex will not run correctly on Mac. Try using provided [virtual machine on Fedora](https://trex-tgn.cisco.com/trex/doc/trex_vm_manual.html).

