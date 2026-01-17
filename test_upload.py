import requests

# Test upload endpoint
url = 'http://localhost:5000/upload'
files = {'file': open('input/test_plan.png', 'rb')}
response = requests.post(url, files=files)
print('Status Code:', response.status_code)
print('Response JSON:', response.json())
