import json
import requests

#r = requests.get(adresseServeur+"/", data=json.dumps({"name": ["foo", "poo", "koo"]}))
r = requests.get(adresseServeur+"/coucou?arg1=toto&arg2=" + json.dumps({"name": ["foo", "poo", "koo"]}))
print(r.text)

