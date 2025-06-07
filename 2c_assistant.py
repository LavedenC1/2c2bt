#!/usr/bin/env python3
import sys
import subprocess
import threading
import logging
import time

from flask import Flask
from modules.recognizeSpeech import recognize_speech
from modules.sendMessageToAI import sendMessageToAI
from modules.getConf import getConf

import requests
if getConf()['kb_lib'] == "pynput":
    from pynput import keyboard
elif getConf()['kb_lib'] == "keyboard":
    import keyboard


def start_ai():
    try:
        requests.get("http://127.0.0.1:54765/open")
        chat_messages = [{"role": "system", "content": getConf()['sys_prompt']}]
        config = getConf()

        if config['include_context']["home_directory"]:
            chat_messages.append({
                "role": "user",
                "content": "$$ CONTEXT $ HOME DIRECTORY $$ " + config['include_context']["home_directory"]
            })
        if config['include_context']["system_info"]:
            chat_messages.append({
                "role": "user",
                "content": "$$ CONTEXT $ SYSTEM INFO $$ " + config['include_context']["system_info"]
            })
        if config['include_context']["directories"]:
            for path in config['include_context']["directories"]:
                result = subprocess.run(
                    ['ls', '-al', path],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True
                )
                chat_messages.append({
                    "role": "user",
                    "content": "$$ CONTEXT $ DIRECTORY $$ " + result.stdout
                })
        if config['custom_context']:
            for item in config['custom_context']:
                chat_messages.append({
                    "role": "user",
                    "content": "$$ CONTEXT $ CUSTOM USER CONTEXT $$ " + item
                })

        api_keys = config['api_keys']

        requests.post("http://127.0.0.1:54765/msg",data="Please wait for voice recognition model is loaded. This may take a few seconds...")

        text = recognize_speech()
        try:
            if text[0] == False:
                requests.post("http://127.0.0.1:54765/msg",data=text[1])
                time.sleep(getConf().get('exit_delay'))
                requests.get("http://127.0.0.1:54765/close")
                return
        except:
            pass
        if text is None:
            requests.post("http://127.0.0.1:54765/msg",data="No speech recognized.")
            time.sleep(getConf().get('exit_delay'))
            requests.get("http://127.0.0.1:54765/close")
            return
        if text == "":
            requests.post("http://127.0.0.1:54765/msg",data="No speech recognized.")
            time.sleep(getConf().get('exit_delay'))
            requests.get("http://127.0.0.1:54765/close")
            return

        text = text.strip()
        if text.lower() in ("exit", "quit", "stop"):
            requests.post("http://127.0.0.1:54765/msg",data="Exiting...")
            sys.exit(0)
        
        

        requests.post("http://127.0.0.1:54765/msg",data=f"You said: {text}")
        chat_messages.append({"role": "user", "content": text})

        command = sendMessageToAI(chat_messages, api_keys, config['ai_model'], temperature=0.0)
        try:
            if command[0] == False:
                requests.post("http://127.0.0.1:54765/msg",data=command[1])
                time.sleep(getConf().get('exit_delay'))
                requests.get("http://127.0.0.1:54765/close")
                return
        except:
            pass
        requests.post("http://127.0.0.1:54765/msg",data=f"Generated command:\n{command}")

        choice = requests.post("http://127.0.0.1:54765/msg",data="prompt_yn Would you like to execute the command?").text.strip().lower()
        if choice == 'y':
            try:
                result = subprocess.run(
                    command, shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True
                )
                output = result.stdout if result.stdout else result.stderr
                requests.post("http://127.0.0.1:54765/msg",data="Command output:")
                requests.post("http://127.0.0.1:54765/msg",data=output)
                time.sleep(getConf().get('exit_delay'))
                requests.get("http://127.0.0.1:54765/close")
            except Exception as e:
                requests.post("http://127.0.0.1:54765/msg",data=f"Error running command: {e}")
                time.sleep(getConf().get('exit_delay'))
                requests.get("http://127.0.0.1:54765/close")
        else:
            requests.post("http://127.0.0.1:54765/msg",data="Aborting!")
            time.sleep(getConf().get('exit_delay'))
            requests.get("http://127.0.0.1:54765/close")
    except requests.exceptions.ConnectionError as e:
        print("Server not running!")

if __name__ == '__main__':
    if getConf()['kb_lib'] == "pynput":
        hotkey = getConf()['pynput_kbs']
        hotkey_actions = {
            hotkey: lambda: threading.Thread(target=start_ai, daemon=True).start()
            # "<esc>": lambda: listener.stop()
        }

        with keyboard.GlobalHotKeys(hotkey_actions) as listener:
            listener.join()
    elif getConf()['kb_lib'] == "keyboard":
        print("Make sure 2c_kb_lib.py is running!")

        app = Flask(__name__)

        @app.route('/start_ai', methods=['GET'])
        def start_ai_route():
            threading.Thread(target=start_ai, daemon=True).start()
            return "AI started", 200
        
        app.run(host='127.0.0.1', port=54766, debug=True)