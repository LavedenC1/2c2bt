import os
import json
import requests
import sounddevice as sd
import speech_recognition as sr
from vosk import Model, KaldiRecognizer, SetLogLevel
from modules.getConf import getConf
from modules.downloadModel import downloadModel

def recognize_speech():
    SetLogLevel(-1)

    try:
        homedir = os.path.expanduser("~")
        model_type = getConf()['voice_model']

        # Determine model path based on configuration
        model_path = {
            "vosk_giga": f"{homedir}/vmodels/vosk-model-en-us-0.42-gigaspeech",
            "vosk_big": f"{homedir}/.vmodels/vosk-model-en-us-0.22",
            "vosk_medium": f"{homedir}/.vmodels/vosk-model-en-us-0.22-lgraph",
            "vosk_small": f"{homedir}/.vmodels/vosk-model-small-en-us-0.15",
            "cmu_sphinx": homedir
        }.get(model_type)

        if not model_path:
            requests.post("http://127.0.0.1:54765/msg", data="Invalid model type in config.json")
            return False, "Invalid model type"

        if model_type.startswith("vosk_") and not os.path.exists(model_path):
            requests.post("http://127.0.0.1:54765/msg", data=f"Model not found at {model_path}. Downloading...")
            downloadModel(model_type)

        r = sr.Recognizer()
        sample_rate = int(sd.query_devices(sd.default.device[0], 'input')['default_samplerate'])

        if model_type.startswith("vosk_"):
            model = Model(model_path)
            recognizer = KaldiRecognizer(model, sample_rate)

            with sr.Microphone(sample_rate=sample_rate) as source:
                requests.post("http://127.0.0.1:54765/msg", data="Listening...")
                audio = r.listen(source)
                audio_data = audio.get_raw_data()

            if recognizer.AcceptWaveform(audio_data):
                result = recognizer.Result()
                text = json.loads(result)['text']
            else:
                partial_result = json.loads("".join(recognizer.PartialResult()))
                text = partial_result['partial']

            return text

        elif model_type == "cmu_sphinx":
            with sr.Microphone(sample_rate=sample_rate) as source:
                requests.post("http://127.0.0.1:54765/msg", data="Listening...")
                audio = r.listen(source)

            try:
                text = r.recognize_sphinx(audio)
                return text
            except sr.UnknownValueError:
                return ""

    except sr.RequestError as e:
        requests.post("http://127.0.0.1:54765/msg", data=f"Could not get results; {e}")
    except FileNotFoundError:
        requests.post("http://127.0.0.1:54765/msg", data=f"Error: Model not found at {model_path}.")
