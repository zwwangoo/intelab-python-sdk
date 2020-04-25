import socket
import json
import urllib.request
import urllib.parse
from urllib.error import HTTPError
from .logger import log


def get_host_ip():
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
    if not ip:
        raise socket.gaierror(-2, 'Name or service not known')
    return ip


def do_request(method, url, data={},
               headers={'Content-Type': 'application/json'}):
    if method == 'GET' or method == 'DELETE':
        data = urllib.parse.urlencode(data)
        if data:
            url = url + '?' + data
        data = None
    else:
        data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(url, data, headers, method=method)
    try:
        response = urllib.request.urlopen(req)
        res_json = json.loads(response.read().decode('utf-8'))
    except HTTPError as e:
        log.error(e)
    except ValueError as e:
        log.error('JSONDecodeError.[{}]'.format(e))
    else:
        return res_json
