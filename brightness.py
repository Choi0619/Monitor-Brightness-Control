import tkinter as tk
from tkinter import ttk
import screen_brightness_control as sbc

def set_brightness_from_scale(value):
    brightness_entry.delete(0, tk.END)
    brightness_entry.insert(0, str(round(float(value))))
    sbc.set_brightness(round(float(value)))
    update_current_brightness()

def set_brightness_from_entry(event=None):
    try:
        brightness_value = int(brightness_entry.get())
        brightness_value = max(0, min(brightness_value, 100))
        sbc.set_brightness(brightness_value)
        brightness_scale.set(brightness_value)
        update_current_brightness()
    except ValueError:
        pass

def update_current_brightness():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Current brightness levels:\n")
    for monitor in sbc.list_monitors():
        current_brightness = sbc.get_brightness(display=monitor)
        result_text.insert(tk.END, f"{monitor}: {current_brightness}%\n")
    result_text.config(state=tk.DISABLED)

def set_initial_brightness():
    try:
        # Get the brightness of the primary monitor and set scale and entry values accordingly
        current_brightness = sbc.get_brightness()[0]
        brightness_scale.set(current_brightness)
        brightness_entry.delete(0, tk.END)
        brightness_entry.insert(0, str(current_brightness))
    except Exception as e:
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END, f"Error getting brightness: {e}\n")
        result_text.config(state=tk.DISABLED)

def adjust_brightness_from_button():
    set_brightness_from_entry()  # Adjust brightness based on the value entered in the text field

def adjust_brightness_with_gui():
    root = tk.Tk()
    root.title("Brightness Adjuster")
    root.geometry("350x400")

    style = ttk.Style()
    style.configure("TScale", background="#f0f0f0")
    
    title_label = tk.Label(root, text="Monitor Brightness Adjuster", font=("Arial", 14, "bold"), pady=10)
    title_label.pack()

    # Scale for adjusting brightness
    global brightness_scale
    brightness_scale = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=300, command=set_brightness_from_scale)
    brightness_scale.pack(pady=10)

    # Entry for manually inputting brightness
    global brightness_entry
    brightness_entry = tk.Entry(root, justify="center", font=("Arial", 12))
    brightness_entry.pack(pady=5)
    brightness_entry.bind("<Return>", set_brightness_from_entry)

    adjust_button = ttk.Button(root, text="Adjust Brightness", command=adjust_brightness_from_button)
    adjust_button.pack(pady=5)

    global result_text
    result_text = tk.Text(root, height=10, width=35, wrap=tk.WORD)
    result_text.pack(padx=10, pady=10)
    result_text.insert(tk.END, "Current brightness levels:\n")
    result_text.config(state=tk.DISABLED)

    set_initial_brightness()

    root.mainloop()

if __name__ == "__main__":
    adjust_brightness_with_gui()
