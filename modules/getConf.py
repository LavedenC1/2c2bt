import json
import sys

def getConf():
    from pathlib import Path
    path = Path(str(sys.executable)).parent.parent.parent
    with open(f"{path}/config.json","r") as f:
        data = json.loads(f.read())

    return data