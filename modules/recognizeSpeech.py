from pathlib import Path
import sys
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
        conf = getConf()
        model_type = conf['voice_model']

        model_path = {
            "vosk_giga": f"{homedir}/vmodels/vosk-model-en-us-0.42-gigaspeech",
            "vosk_big": f"{homedir}/.vmodels/vosk-model-en-us-0.22",
            "vosk_medium": f"{homedir}/.vmodels/vosk-model-en-us-0.22-lgraph",
            "vosk_small": f"{homedir}/.vmodels/vosk-model-small-en-us-0.15",
            "cmu_sphinx": homedir,
            "google_cloud": homedir
        }.get(model_type)

        if not model_path:
            requests.post("http://127.0.0.1:54765/msg", data="Invalid model type in config.json")
            return False, "Invalid model type"

        if model_type.startswith("vosk_") and not os.path.exists(model_path):
            requests.post("http://127.0.0.1:54765/msg", data=f"Model not found at {model_path}. Downloading...")
            downloadModel(model_type)

        r = sr.Recognizer()
        device_info = sd.query_devices(kind='input')
        sample_rate = int(device_info['default_samplerate'])

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
                requests.post("http://127.0.0.1:54765/msg", data="Processing...")
                text = r.recognize_sphinx(audio)
                return text
            except sr.UnknownValueError:
                return ""

        elif model_type == "google_cloud":
            path = Path(str(sys.executable)).parent.parent.parent
            key_file = conf['googlec_key_file']
            key_path = f"{path}/{key_file}"

            if not os.path.exists(key_path):
                requests.post("http://127.0.0.1:54765/msg", data=f"Google Cloud key file not found at {key_path}")
                return False, "Google Cloud key file not found"

            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

            with sr.Microphone(sample_rate=sample_rate) as source:
                requests.post("http://127.0.0.1:54765/msg", data="Listening...")
                audio = r.listen(source)

            try:
                requests.post("http://127.0.0.1:54765/msg", data="Processing...")
                text = r.recognize_google_cloud(audio)
                return text
            except sr.UnknownValueError:
                return False, "Google Cloud could not understand audio"
            except sr.RequestError as e:
                return False, f"Could not request results from Google Cloud; {e}"

        return False, "No valid speech recognition engine selected"

    except sr.RequestError as e:
        requests.post("http://127.0.0.1:54765/msg", data=f"Could not get results; {e}")
        return False, str(e)
    except FileNotFoundError:
        requests.post("http://127.0.0.1:54765/msg", data=f"Error: Model not found at {model_path}.")
        return False, f"Model not found at {model_path}"
