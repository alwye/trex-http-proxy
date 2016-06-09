# TRex HTTP Proxy
## Overview
This HTTP Proxy allows you to integrate TRex traffic generator (https://trex-tgn.cisco.com) into HTTP environment. For example, it is convenient way to manage the TRex instance via web interface.

## Prerequisites
Run the following command to install required packages:

```
pip install -r requirements.txt
```

## Possible problems
### dnet library on Mac
If you see this message:

```
Could not find a version that satisfies the requirement dnet (from versions: )
No matching distribution found for dnet
```

Try this commands:

```
brew install --with-python libdnet
pip install pcapy
pip install scapy
```