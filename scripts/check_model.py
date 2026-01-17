import urllib.request
url='http://127.0.0.1:5000/output/model.glb'
req=urllib.request.Request(url, method='GET')
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        print('Status', r.status)
        print('Content-Type:', r.getheader('Content-Type'))
        print('Content-Length:', r.getheader('Content-Length'))
        data = r.read(64)
        print('First bytes:', data[:8])
except Exception as e:
    print('ERROR', e)
