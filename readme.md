# 2c2bt Voice Assistant
A voice assistant designed to help with linux!
## Information
2c2bt runs on python, using OpenRouter to serve AI. It currently has a basic GUI (tbi) and is activated through a keyboard shortcut. It was made for Linux, but could be tweaked for Windows or Mac. Also this is a long readme.
## Setup
1. Clone the repo and enter the directory
```bash
git  clone  https://github.com/LavedenC1/2c2bt
cd  2c2bt
```
2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Install all packages
```bash
pip3 install -r requirements.txt
```
### Without Systemd
4. Run both scripts at the same time
```bash
python3 main.py # One terminal
python3 gui_server.py # Another terminal
```
5. Configure the project in the **Config** section
### With Systemd
4. Now here is the hard part.
| Only works if your system uses systemd

- Create a new systemd service:
```bash
sudo nano /etc/systemd/system/2c2bt_gui.service
```
- Paste this in, make sure your values are right
```ini
[Unit]
Description=2c2bt GUI Server
After=network.target

[Service]
ExecStart=/path/to/your/.venv/python3 /path/to/project/gui_server.py
WorkingDirectory=/path/to/project
Restart=always
; Find your user: `echo $USER`
User=user

[Install]
WantedBy=multi-user.target
```
| Did you make sure your paths and username is right?
- Then restart the systemd daemon
```bash
sudo systemctl daemon-reload
```
- Now enable it on boot (optional) and start it
```bash
sudo systemctl enable --now 2c2bt_gui.service # If you want to enable on boot
sudo systemctl start 2c2bt_gui.service
```
- If anything goes wrong, restart the server like this:
```bash
sudo systemctl restart 2c2bt_gui.service
```
- That's the server, now to make the assistant enabler.
- Create a new systemd service, but for the user
```bash
mkdir -p ~/.local/share/systemd/user
nano ~/.local/share/systemd/user/2c2bt_assistant.service
```
- Paste this in, make sure the info is right too.
```ini
[Unit]
Description=2c2bt Assistant Service

[Service]
Type=oneshot
ExecStart=/path/to/your/.venv/python3 /path/to/project/main.py
WorkingDirectory=/path/to/project/
RemainAfterExit=true
StandardOutput=journal

[Install]
WantedBy=graphical-session.target
```
- Restart the daemon again
```bash
sudo systemctl daemon-reload
```
- Now enable it
```bash
sudo systemctl enable --user 2c2bt_assistant.service # If you want to enable after login
sudo systemctl start 2c2bt_assistant.service
```
- And restart it like this
```bash
sudo systemctl restart --user 2c2bt_assistant.service
```
- And that's the hard part.
5. Configure the project in the **Config** section

## Config
The config is in config.json at the project root. It is in JSON.
### Configuration Values:
1. `voice_model`
	- The voice model to use.
	- Use the model that fits your device in computing power
	- The deeper the list, the more intensive, the more time to load the model.
	- Offline models:
		- `cmu_sphinx` -> CMU Sphinx. Very light and inaccurate.
		- `vosk_small` -> Vosk's small model (~40MB). Light, but more accurate
		- `vosk_medium` -> Vosk's lgraph model (~128MB). Not as light, but more accurate.
		- `vosk_big` -> Vosk's generic model (~1.8G). Heavy, but much more accurate
		- `vosk_giga` -> Vosk's gigamodel ~(2.3G). Be pacient, very heavy, but also accurate.
	- Online models:
		- None
2. `sudo_password`
	- Your sudo password.
	- This isn't sent anywhere and is local on the device.
	- Used for the sudo converter.
	- Type: String
3. `pwless_sudo_converter`
	- Remove the need to type in your password when using sudo commands.
	- Gets sudo password from `sudo_password`
	- Example:
		- `sudo apt update` -> `echo <password> | sudo -S apt update`
	- Type: Boolean
4. `ai_model`
	- The AI model to use for the LLM, can be found [here](https://openrouter.ai/models?max_price=0).
	- Example: `deepseek/deepseek-prover-v2:free`
	- Type: String
5. `sys_prompt`
	- The system prompt of the model
	- Recommended not to change!
	- Type: String
6. `exit_delay`
	- The time in seconds to close the GUI after the task has completed (error or not)
	- Type: Int
7. `include_context`
	- Include information about `home_directory`, `system_information`, and `directories`.
	- Find your home directory like this: `echo $HOME`
	- Get your system information like this: `uname -a`
		- You can use other commands to get more detailed system information, or you can type it out.
	- And include directories by adding their path
		- The context for directory is basically `ls -al <path>`
	- Note: This is all sent to the LLM.e
	- Type: JSON
8. `custom_context`
	- Context you would like to include.
	- You can type this out and make as much as you want
	- For example:
		- `My system is dual-boot`
		-  `I'm new to Linux`
		- `I live in the United States`
		- ...
	- It is recommended to add `No stdin is passed in`
9. `api_keys`
	- Your Openrouter API key(s).
	- ~~You can use multiple account to get more requests on free models and avoid being rate limited~~
	- Get an API Key from [here](https://openrouter.ai/settings/keys)
10. `keyboard_shortcut`
	- The activation keyboard shortcut.
	- In Pynput notation
	- Examples:
		- `<ctrl>+<shift>+e`
		- `<alt>+<shift>+a`
		- `<esc>+a`
### After configuring:
If you are using systemd, restart the service:
```bash
sudo systemctl restart --user 2c2bt_assistant.service
```
Otherwise, just rerun the `main.py` script.
 
## Usage
After all the configuration and setup, use the keyboard shortcut you setup to start the assistant. A small GUI will pop up at the bottom left of the screen, and start speaking when it says `Listening`.<br>
After you are done speaking, give the model a moment to convert your speech to natural english, then confirm with the **Yes** or **No** button if you want to run the command

## Credits
- Thanks to Mr. Poole for encouraging me to become better at computer science!
- Thanks to my friends for being supportive!