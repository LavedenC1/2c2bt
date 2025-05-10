#!/usr/bin/env python3
import sys
import subprocess
import threading
import logging

from pynput import keyboard
from modules.recognizeSpeech import recognize_speech
from modules.sendMessageToAI import sendMessageToAI
from modules.getConf import getConf

from PyQt5 import QtWidgets, QtGui, QtCore


def start_ai():
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

    print("Please wait for voice recognition model is loaded. This may take a few seconds...")

    text = recognize_speech()
    if text is None:
        print("No speech recognized.")
        return
    if text == "":
        print("No speech recognized.")
        return

    text = text.strip()
    if text.lower() in ("exit", "quit", "stop"):
        print("Exiting...")
        sys.exit(0)

    print(f"You said: {text}")
    chat_messages.append({"role": "user", "content": text})

    command = sendMessageToAI(chat_messages, api_keys, config['ai_model'], temperature=0.0)
    print(f"Generated command:\n{command}")

    choice = input("Would you like to execute the command? [y/N]: ").strip().lower()
    if choice == 'y':
        try:
            result = subprocess.run(
                command, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True
            )
            output = result.stdout if result.stdout else result.stderr
            print("Command output:")
            print(output)
        except Exception as e:
            print(f"Error executing command: {e}")
    else:
        print("Command execution skipped.")

if __name__ == '__main__':
    hotkey = getConf()['keyboard_shortcut']
    hotkey_actions = {
        hotkey: lambda: threading.Thread(target=start_ai, daemon=True).start()
    }

    with keyboard.GlobalHotKeys(hotkey_actions) as listener:
        listener.join()
