# 2c2bt Voice Assistant
A voice assistant designed to help with linux!
## Information
2c2bt runs on python, using OpenRouter/OpenAI to serve AI. It currently has a basic GUI (tbi) and is activated through a keyboard shortcut. It was made for Linux, but could be tweaked for Windows or Mac. Also this is a long readme.
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
| You will need a virtual environment, the project will error out without it!

3. Install all packages
```bash
pip3 install -r requirements.txt
```
### Without XDG
4. Run both scripts at the same time
```bash
python3 2c_assistant.py # One terminal
python3 2c_gui_server.py # Another terminal
python3 2c_gui_kb.py # If you are using keyboard 
```
5. Configure the project in the **Config** section
### With XDG
4. Now here is the hard part.
| Only works if your system uses XDG

- Create a new desktop file:
```bash
nano ~/.config/autostart/2c2bt_gui.desktop
```
- Paste this in, make sure your values are right:
```ini
[Desktop Entry]
Type=Application
Name=2c2bt GUI Server
Exec=/path/to/project/.venv/bin/python3 /path/to/project/2c_gui_server.py
WorkingDirectory=/path/to/project
Terminal=false
X-GNOME-Autostart-enabled=true
```
| Did you make sure your paths is right?
- Make it executable
```bash
chmod +x ~/.config/autostart/2c2bt_gui.desktop
```
- If anything goes wrong, restart the server by relogging in or like this:
```bash
kill $(ps -aux | grep 2c_gui_server.py | awk 'NR==1 {print($2)}')
gio launch ~/.config/autostart/2c2bt_gui.desktop >/dev/null 2>&1
```
| Yes you can make a script to automate this
- That's the server, now to make the assistant enabler.
- Create a new desktop file, but for the assistant
```bash
nano ~/.config/autostart/2c2bt_assistant.desktop
```
- Paste this in, make sure the info is right too.
```ini
[Desktop Entry]
Type=Application
Name=2c2bt Assistant
Exec=/path/to/project/.venv/bin/python3 /path/to/project/2c_assistant.py
WorkingDirectory=/path/to/project
Terminal=false
X-GNOME-Autostart-enabled=true
```
- Make it executable
```bash
chmod +x ~/.config/autostart/2c2bt_assistant.desktop
```
- And restart it like this
```bash
kill $(ps -aux | grep 2c_assistant.py | awk 'NR==1 {print($2)}')
gio launch ~/.config/autostart/2c2bt_assistant.desktop >/dev/null 2>&1
```

- **Only do this part if you are using keyboard library (more in config section)**
- Edit `kb_lib_wrapper.sh` in the project directory. Replace $SUDO_PW with your sudo password and make sure the path to the python executable in the virtual environment and the path to the `2c_kb_lib.py` is correct
- Make it executable
```bash
chmod +x kb_lib_wrapper.sh
```
- Create a new desktop file, but for the keyboard library listener
```bash
nano ~/.config/autostart/2c2bt_kbl.desktop
```
- Paste this in, make sure the info is right too.
```ini
[Desktop Entry]
Type=Application
Name=2c2bt Keyboard Library Wrapper
Exec=/path/to/project/kb_lib_wrapper.sh
WorkingDirectory=/path/to/project
Terminal=false
X-GNOME-Autostart-enabled=true
```
- Make it executable
```bash
chmod +x ~/.config/autostart/2c2bt_kbl.desktop
```
- And restart it like this
```bash
sudo kill $(ps -aux | grep 2c_kb_lib.py | awk 'NR==1 {print($2)}')
gio launch ~/.config/autostart/2c2bt_kbl.desktop >/dev/null 2>&1
```
- And that's the hard part.
5. Configure the project in the **Config** section

## Create a stop and start command
Create a stop and start command to avoid typing long kill commands. Two methods, in your `.bashrc` or a custom command.
### .bashrc
Add this to your `.bashrc`:
```bash
function 2c2bt(){
    if [ "$1" == "-s" ]; then
        echo "Starting 2c2bt"
        gio launch ~/.config/autostart/2c2bt_gui.desktop >/dev/null 2>&1
        gio launch ~/.config/autostart/2c2bt_assistant.desktop >/dev/null 2>&1
		# gio launch ~/.config/autostart/2c2bt_kbl.desktop >/dev/null 2>&1 # Uncomment if using keyboard library
        echo "Done"
    elif [ "$1" == "-k" ]; then
        echo "Killing"
        kill $(ps -aux | grep 2c_gui_server.py | awk 'NR==1 {print($2)}')
        kill $(ps -aux | grep 2c_assistant.py | awk 'NR==1 {print($2)}')
		# echo $SUDO_PW | sudo -S kill $(ps -aux | grep 2c_kb_lib.py | awk 'NR==1 {print($2)}') # If using keyboard library. replace your sudo password
        echo "Done"
    elif [ "$1" == "-r" ]; then
        echo "Killing"
        kill $(ps -aux | grep 2c_gui_server.py | awk 'NR==1 {print($2)}')
        kill $(ps -aux | grep 2c_assistant.py | awk 'NR==1 {print($2)}')
		# echo $SUDO_PW | sudo -S kill $(ps -aux | grep 2c_kb_lib.py | awk 'NR==1 {print($2)}') # If using keyboard library. replace your sudo password
        echo "Starting 2c2bt"
        gio launch ~/.config/autostart/2c2bt_gui.desktop >/dev/null 2>&1
        gio launch ~/.config/autostart/2c2bt_assistant.desktop >/dev/null 2>&1
        # gio launch ~/.config/autostart/2c2bt_kbl.desktop >/dev/null 2>&1 # Uncomment if using keyboard library
        echo "Done"
    else
        echo -e "Usage: 2c2bt [option]\n -s    Start 2c2bt\n -k    Kill 2c2bt\n -r    Restart 2c2bt"
    fi
}

_2c2bt_comp() {
    local cur prev
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    local commands=""
    local options="-k -s -r"
    COMPREPLY=($(compgen -W "$commands $options" -- "$cur"))
}

complete -F _2c2bt_comp 2c2bt
```
The command is completed, now just reload the shell to take effect:
```bash
source ~/.bashrc
```
### Command
1. Create a new file, name it `2c2bt`.
```bash
touch 2c2bt
```
3. Paste this in:
```bash
#!/bin/bash
if [ "$1" == "-s" ]; then
    echo "Starting 2c2bt"
    gio launch ~/.config/autostart/2c2bt_gui.desktop >/dev/null 2>&1
    gio launch ~/.config/autostart/2c2bt_assistant.desktop >/dev/null 2>&1
    # gio launch ~/.config/autostart/2c2bt_kbl.desktop >/dev/null 2>&1 # Uncomment if using keyboard library
    echo "Done"
elif [ "$1" == "-k" ]; then
    echo "Killing"
    kill $(ps -aux | grep 2c_gui_server.py | awk 'NR==1 {print($2)}')
    kill $(ps -aux | grep 2c_assistant.py | awk 'NR==1 {print($2)}')
    # echo $SUDO_PW | sudo -S kill $(ps -aux | grep 2c_kb_lib.py | awk 'NR==1 {print($2)}') # If using keyboard library. replace your sudo password
    echo "Done"
elif [ "$1" == "-r" ]; then
    echo "Killing"
    kill $(ps -aux | grep 2c_gui_server.py | awk 'NR==1 {print($2)}')
    kill $(ps -aux | grep 2c_assistant.py | awk 'NR==1 {print($2)}')
    # echo $SUDO_PW | sudo -S kill $(ps -aux | grep 2c_kb_lib.py | awk 'NR==1 {print($2)}') # If using keyboard library. replace your sudo password
    echo "Starting 2c2bt"
    gio launch ~/.config/autostart/2c2bt_gui.desktop >/dev/null 2>&1
    gio launch ~/.config/autostart/2c2bt_assistant.desktop >/dev/null 2>&1
    # gio launch ~/.config/autostart/2c2bt_kbl.desktop >/dev/null 2>&1 # Uncomment if using keyboard library
    echo "Done"
else
    echo -e "Usage: 2c2bt [option]\n -s    Start 2c2bt\n -k    Kill 2c2bt\n -r    Restart 2c2bt"
fi
```
4. Allow execution permissions:
```bash
chmod +x 2c2bt
```
5. Move it to `/usr/local/bin`, or wherever your path says:
```bash
sudo mv 2c2bt /usr/local/bin
```
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
	- The AI model to use for the LLM, can be found [here](https://openrouter.ai/models) for OpenRouter.
	- The AI model to use for the LLM, can be found [here](https://platform.openai.com/docs/models) for OpenAI.
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
	- It is recommended to add `No stdin is passed in` and `I am not the root user, but I can use sudo` (if applies)
9. `api_keys`
	- Your Openrouter/OpenAI API key(s).
	- ~~You can use multiple account to get more requests on free models and avoid being rate limited~~
	- Get an API Key from [here](https://openrouter.ai/settings/keys) for OpenRouter.
	- Get an API Key from [here](https://platform.openai.com/api-keys) for OpenAI.
10. `keyboard_shortcut`
	- The activation keyboard shortcut.
	- In Pynput notation
	- Examples:
		- `<ctrl>+<shift>+e`
		- `<alt>+<shift>+a`
		- `<esc>+a`
11. `kb_lib`
	- The keyboard library to detect keypresses.
	- Can be `pynput` or `keyboard`
	- Pynput doesn't need root, but sometimes doesn't work.
	- Keyboard needs root, but always works.
12. `ai_provider`
	- The AI Provider.
	- Can be `openai` or `openrouter`
	- OpenRouter has more models and has free models.
	- OpenAI is only paid but is smarter.
### After configuring:
If you are using XDG, restart the project!:
```bash
kill $(ps -aux | grep 2c_assistant.py | awk 'NR==1 {print($2)}')
gio launch ~/.config/autostart/2c2bt_assistant.desktop
```
Or
```bash
2c2bt -r
```
Otherwise, just rerun the `2c_assistant.py` script.
 
## Usage
After all the configuration and setup, use the keyboard shortcut you setup to start the assistant. A small GUI will pop up at the bottom left of the screen, and start speaking when it says `Listening`.<br>
After you are done speaking, give the model a moment to convert your speech to natural english, then confirm with the **Yes** or **No** button if you want to run the command

## Credits
- Thanks to Mr. Poole for encouraging me to become better at computer science!
- Thanks to my friends for being supportive!