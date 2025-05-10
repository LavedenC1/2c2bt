import logging
import speech_recognition as sr
import json
from vosk import Model, KaldiRecognizer
from modules.getConf import *
from modules.downloadModel import downloadModel
from vosk import SetLogLevel
import os
import sounddevice as sd
import sys

def recognize_speech():
    
    SetLogLevel(-1)

    try:
        homedir = os.path.expanduser("~")

        model_type = getConf()['voice_model']

        if model_type == "giga":
            model_path = f"{homedir}/vmodels/vosk-model-en-us-0.42-gigaspeech"
        elif model_type == "big":
            model_path = f"{homedir}/.vmodels/vosk-model-en-us-0.22"
        elif model_type == "medium":
            model_path = f"{homedir}/.vmodels/vosk-model-en-us-0.22-lgraph"
        elif model_type == "small":
            model_path = f"{homedir}/.vmodels/vosk-model-small-en-us-0.15"
        else:
            print("Pick a model from small, medium, big, or giga in config.json")
            return "Invalid model type"
        
        if not os.path.exists(model_path):
            print(f"Model not found at {model_path}. Downloading...")
            downloadModel(model_type)
        
        model = Model(model_path)
        recognizer = KaldiRecognizer(model, int(sd.query_devices(sd.default.device[0], 'input')['default_samplerate']))

        r = sr.Recognizer()
        with sr.Microphone(sample_rate=int(sd.query_devices(sd.default.device[0], 'input')['default_samplerate'])) as source:
            print("What would you like me to do?")
            audio = r.listen(source)
            audio_data = audio.get_raw_data()

        if recognizer.AcceptWaveform(audio_data):
            result = recognizer.Result()
            text = json.loads(result)['text']
        else:
            # print("No final result, but partial results can be seen.")
            partial_result = json.loads("".join(recognizer.PartialResult()))
            # print(recognizer.PartialResult())
            text = partial_result['partial']

        return text

    except sr.RequestError as e:
        print(f"Could not request results from Vosk service; {e}")
    except FileNotFoundError:
        print(f"Error: Vosk model not found at {model_path}. Please download and extract a model.")

if __name__ == "__main__":
    print(recognize_speech())