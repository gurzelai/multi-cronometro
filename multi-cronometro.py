import tkinter as tk
import time
import shelve
from tkinter import messagebox

def ventana_opciones():   
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    width = 850
    height = 65
    x = (screen_width/2) - (width/2)
    y = (screen_height/4) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))


def on_closing():
    global running
    running = False
    with shelve.open("timer_data") as data:
        data["elapsed_time"] = elapsed_time
        data["name"] = name_entry.get()
    
    root.destroy()

root = tk.Tk()
root.title("Cronometro")
root.protocol("WM_DELETE_WINDOW", on_closing)

with shelve.open("timer_data") as data:
    elapsed_time = data.get("elapsed_time", 0)
    name = data.get("name", "")

ventana_opciones()

def start_timer():
    global running, elapsed_time
    running = False
    
    print(elapsed_time)
    
    if not running:
        start_time = time.time() - elapsed_time
    else:
        start_time = time.time()
    running = True
    while running:
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        timer_label.config(text=formatted_time)
        root.update()
        
start_button = tk.Button(root, text="Iniciar Cronómetro",  command=start_timer)
start_button.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)

def stop_timer():
    global running
    running = False
    
stop_button = tk.Button(root, text="Detener Cronómetro", command=stop_timer)
stop_button.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)

formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
timer_label = tk.Label(root, text= formatted_time , font=("Arial", 24))
timer_label.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=5)

def reset_timer():
    global elapsed_time, running
    if messagebox.askyesno("Reiniciar cronómetro", "¿Estás seguro de que deseas reiniciar el cronómetro?"):
        running = False
        elapsed_time = 0
        timer_label.config(text="00:00:00")

reset_button = tk.Button(root, text="Resetear Cronómetro", command=reset_timer)
reset_button.grid(row=0, column=3, padx=5, pady=5, ipadx=5, ipady=5)

name_entry = tk.Entry(root)
name_entry.grid(row=0, column=4, padx=5, pady=5, ipadx=5, ipady=5)
name_entry.insert(0, name)



root.mainloop()