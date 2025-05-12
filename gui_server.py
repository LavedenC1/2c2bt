from flask import Flask, request
import tkinter as tk
import threading
from tkinter import font

global text
text = ""

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/msg", methods=["POST"])
def receive_data():
    global text
    body = request.get_data(as_text=True)
    text = text + body + "\n"
    window.after(0, lambda: label.config(text=text))
    return body

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

def run_flask_app():
    app.run(debug=True, use_reloader=False)

# Create Tkinter GUI with custom styling
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

# Create a custom font for the label
custom_font = font.Font(family="Monospace", size=8, weight="normal")

label = tk.Label(window, text="", anchor="nw", justify="left",
                 bg="#343E3D", fg="#6EEB83", font=custom_font,
                 padx=10, pady=10, relief="groove")
label.pack(fill="both", expand=True, padx=10, pady=10)

def update_wrap_length(event):
    # Update the wraplength so that text wraps within the label with some padding
    label.config(wraplength=event.width - 20)

window.bind("<Configure>", update_wrap_length)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    window.mainloop()