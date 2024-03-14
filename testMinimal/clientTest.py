import json
import requests

#r = requests.get("http://127.0.0.1:5000/", data=json.dumps({"name": ["foo", "poo", "koo"]}))
r = requests.get("http://127.0.0.1:5000/coucou?arg1=toto&arg2=" + json.dumps({"name": ["foo", "poo", "koo"]}))
print(r.text)

