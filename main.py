import os
import time

from dotenv import load_dotenv
import requests

load_dotenv()

ROUTER_HOST = os.environ['ROUTER_HOST']
ROUTER_USERNAME = os.environ['ROUTER_USERNAME']
ROUTER_PASSWORD = os.environ['ROUTER_PASSWORD']
SERVER_HOST = os.environ['SERVER_HOST']
SERVER_PORTS = os.environ['SERVER_PORTS']

def get_session_key(url):
    for _ in range(3):
        virtual_servers_page = requests.get(url)
        time.sleep(0.1)
    return virtual_servers_page.text.split('&sessionKey=')[1].split('\';')[0]

def remove_server(url, session_key, host, ports):
    request_model = requests.models.PreparedRequest()
    params = {
        'action': 'remove',
        'rmLst': ''.join(['{host}|{port}|{port}|TCP or UDP|{port}|{port},'.format(host=host, port=port) for port in ports]),
        'sessionKey': session_key
    }
    request_model.prepare_url(url, params)
    requests.get(request_model.url)

def add_server(url, session_key, host, ports):
    request_model = requests.models.PreparedRequest()
    ports_string = ','.join(ports) + ','
    params = {
        'action': 'add',
        'srvName': 'www',
        'dstWanIf': 'ppp0.3',
        'srvAddr':  host,
        'loopBack': '1',
        'proto': '0,0,',
        'eStart': ports_string,
        'eEnd': ports_string,
        'iStart': ports_string,
        'iEnd': ports_string,
        'sessionKey': session_key
    }
    request_model.prepare_url(url, params)
    requests.get(request_model.url)

def main():
    url = 'http://{}:{}@{}/scvrtsrv.cmd'.format(ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_HOST)
    ports = SERVER_PORTS.split(',')

    session_key = get_session_key(url)
    remove_server(url, session_key, SERVER_HOST, ports)

    session_key = get_session_key(url)
    add_server(url, session_key, SERVER_HOST, ports)

if __name__ == "__main__":
    main()
