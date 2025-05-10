import easygui

def update_log(log_text,new_text):
    log_text += new_text + "\n"
    log_text = easygui.textbox("Log", "AI Voice Assistant", log_text)
    return log_text