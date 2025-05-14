from flask import Flask, request
import tkinter as tk
import threading
from tkinter import font

window = tk.Tk()
window.title("2c2bt")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 320
window_height = 500
x = 0
y = screen_height - window_height
window.geometry(f'{window_width}x{window_height}+{x}+{y}')
window.overrideredirect(True)

window.configure(bg="#3772FF")

custom_font = font.Font(family="Monospace", size=8, weight="normal")

label = tk.Label(window, text="", anchor="nw", justify="left",
                 bg="#343E3D", fg="#6EEB83", font=custom_font,
                 padx=10, pady=10, relief="groove")

label.pack(fill="both", expand=True, padx=10, pady=10)
window.after(0, lambda: label.config(text=""))
window.update()
button_frame = tk.Frame(window, bg="#3772FF")
button_frame.pack(pady=5)

window.withdraw()

def command_response_yes():
    answer_var.set("y")

def command_response_no():
    answer_var.set("n")

btn_yes = tk.Button(button_frame, text="Yes", command=command_response_yes)
btn_no = tk.Button(button_frame, text="No", command=command_response_no)

btn_yes.pack(side="left", padx=5)
btn_no.pack(side="left", padx=5)

def update_wrap_length(event):
    label.config(wraplength=event.width - 20)

window.bind("<Configure>", update_wrap_length)


global text
text = ""

# Create a global tkinter variable to capture the answer
answer_var = tk.StringVar()

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/msg", methods=["POST"])
def receive_data():
    global text
    body = request.get_data(as_text=True)
    args = body.split()  # note: use split() to actually get tokens
    if len(args) > 0 and args[0] == "prompt_yn":
        answer_var.set("")
        window.deiconify()
        text = text + " ".join(body.split()[1:]) + "\n"
        window.after(0, lambda: label.config(text=text))
        window.wait_variable(answer_var)
        answer = answer_var.get()
        return answer, 200

    text = text + body + "\n"
    window.after(0, lambda: label.config(text=text))
    return body, 200

@app.route("/open")
def openWin():
    global text
    text = ""
    window.deiconify()
    window.update()
    return "OK", 200

@app.route("/close")
def closeWin():
    global text
    text = ""
    window.after(0, lambda: label.config(text=""))
    window.withdraw()
    window.update()
    return "OK", 200

@app.route("/exit")
def exitWin():
    exit(0)

def runFlask():
    app.run(debug=True, use_reloader=False, port=54765)


if __name__ == '__main__':
    flask_thread = threading.Thread(target=runFlask)
    flask_thread.daemon = True
    flask_thread.start()
    window.mainloop()
