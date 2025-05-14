import os
import requests
import zipfile


def downloadModel(model_type):
    def download_file(url, save_path):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status() 

            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            requests.post("http://127.0.0.1:54765/msg",data=f"File downloaded successfully to: {save_path}")
        except requests.exceptions.RequestException as e:
            requests.post("http://127.0.0.1:54765/msg",data=f"Error downloading file: {e}")
        except IOError as e:
             requests.post("http://127.0.0.1:54765/msg",data=f"Error writing to file: {e}")

    def unzip_file(zip_filepath, extract_to_path):
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_to_path)


    homedir = os.path.expanduser("~")

    if model_type == "vosk_giga":
        model_url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip"
        save_name = "vosk-model-en-us-0.42-gigaspeech.zip"
    elif model_type == "vosk_big":
        model_url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
        save_name = "vosk-model-en-us-0.22.zip"
    elif model_type == "vosk_medium":
        model_url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip"
        save_name = "vosk-model-en-us-0.22-lgraph.zip"
    elif model_type == "vosk_small":
        model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        save_name = "vosk-model-small-en-us-0.15.zip"
    
    if not os.path.exists(f"{homedir}/.vmodels"):
        os.makedirs(f"{homedir}/.vmodels")
    
    requests.post("http://127.0.0.1:54765/msg",data="Downloading...")
    download_file(model_url, f"{homedir}/.vmodels/{save_name}")

    requests.post("http://127.0.0.1:54765/msg",data="Unzipping")
    unzip_file(f"{homedir}/.vmodels/{save_name}", f"{homedir}/.vmodels/")

    requests.post("http://127.0.0.1:54765/msg",data="Cleaning up")
    os.remove(f"{homedir}/.vmodels/{save_name}")

if __name__ == "__main__":
    downloadModel("small")