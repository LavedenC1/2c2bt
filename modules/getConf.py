import json

def getConf():
    with open("config.json","r") as f:
        data = json.loads(f.read())

    return data