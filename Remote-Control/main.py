# -- coding: utf-8 --
import sys
import re
try:
    import thread
except ImportError:
    import _thread as thread
import time
import websocket
import ssl
import json
from wakeonlan import send_magic_packet

def sendCmd(ws,keycmd):
    '''
    json cmd format
    cmd = {
        'method' : 'ms.remote.control',
        'params': {
            'Cmd': 'Click',
            'DataOfCmd': 'KEY_MENU',
            'Option': 'false',
            'TypeOfRemote': 'SendRemoteKey'
        }
    }
    '''
    cmddict = { 'method' : 'ms.remote.control' }
    paramdict = { 'Cmd': 'Click', 'DataOfCmd': 'Bogus_KEY', 'Option': 'false','TypeOfRemote': 'SendRemoteKey'}
    paramdict['DataOfCmd'] = keycmd
    cmddict['params'] = paramdict
    json_str = json.dumps(cmddict)
    print(json_str)
    ws.send(json_str)

if __name__ == "__main__":
    send_magic_packet('BC:7E:8B:90:0B:73')
    websocket.enableTrace(True)
    appname = "SamsungTvRemote2"
    base_url = "wss://192.168.0.34:8002/api/v2/channels/samsung.remote.control?name={}&token={}"
    token = "12368079"
    url = base_url.format(appname,token) # e.g. name=SamsungTvRemote2&token=47216513
    print(url)
    ws = websocket.create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE})
    #ws = None
    # bring up menu
    sendCmd(ws,'KEY_POWER')
    time.sleep(5)
    # close the menu
    sendCmd(ws,'KEY_MENU')
    ws.close()