import requests

data = {"temperature": "27.70", "humidity": "54.50", "hic": "28.50"}
requests.post('http://192.168.1.105:8080/store/', data=data)
