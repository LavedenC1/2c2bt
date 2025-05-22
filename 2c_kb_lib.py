import keyboard
import requests
from modules.getConf import getConf

def hotkey_action():
    try:
        r = requests.get("http://127.0.0.1:54766/start_ai")
    except requests.exceptions.ConnectionError as e:
        print("Server not running/reachable.")

keyboard.add_hotkey(getConf()["keyboard_kbs"], hotkey_action)
keyboard.wait()