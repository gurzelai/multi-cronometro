import tkinter as tk
import time
import sqlite3
from tkinter import messagebox

class Cronometro:
    def __init__(self, root, row, app, name='', elapsed_time=0):
        self.root = root
        self.row = row
        self.app = app
        self.elapsed_time = elapsed_time
        self.running = False
        self.name = name
        self.timer_label = tk.Label(root, text="00:00:00", font=("Arial", 24))
        self.name_entry = tk.Entry(root)
        self.init_gui()
        self.name_entry.insert(0, name)
        # self.load_data(name)

    def init_gui(self):
        start_button = tk.Button(self.root, text="Iniciar Cronómetro", command=self.start_timer)
        start_button.grid(row=self.row, column=0, padx=5, pady=5, ipadx=5, ipady=5)

        stop_button = tk.Button(self.root, text="Detener Cronómetro", command=self.stop_timer)
        stop_button.grid(row=self.row, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        reset_button = tk.Button(self.root, text="Reiniciar Cronómetro", command=self.reset_timer)
        reset_button.grid(row=self.row, column=2, padx=5, pady=5, ipadx=5, ipady=5)

        delete_button = tk.Button(self.root, text="Eliminar", command=self.delete_cronometro)
        delete_button.grid(row=self.row, column=3, padx=5, pady=5, ipadx=5, ipady=5)

        self.timer_label.grid(row=self.row, column=4, padx=5, pady=5, ipadx=5, ipady=5)
        self.name_entry.grid(row=self.row, column=5, padx=5, pady=5, ipadx=5, ipady=5)
        

    def create_widgets(self):
        start_button = tk.Button(self.root, text="Iniciar Cronómetro", command=self.start_timer)
        start_button.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)

        stop_button = tk.Button(self.root, text="Detener Cronómetro", command=self.stop_timer)
        stop_button.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        reset_button = tk.Button(self.root, text="Reiniciar Cronómetro", command=self.reset_timer)
        reset_button.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=5)

        self.timer_label.grid(row=0, column=3, padx=5, pady=5, ipadx=5, ipady=5)
        self.name_entry.grid(row=0, column=4, padx=5, pady=5, ipadx=5, ipady=5)

    def start_timer(self):
        self.running = True
        start_time = time.time() - self.elapsed_time if self.running else time.time()
        while self.running:
            self.elapsed_time = time.time() - start_time
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))
            self.timer_label.config(text=formatted_time)
            self.root.update()
            time.sleep(1)

    def stop_timer(self):
        self.running = False

    def reset_timer(self):
        if messagebox.askyesno("Reiniciar cronómetro", "¿Estás seguro de que deseas reiniciar el cronómetro?"):
            self.running = False
            self.elapsed_time = 0
            self.timer_label.config(text="00:00:00")

    def delete_cronometro(self):
        if messagebox.askyesno("Eliminar", "¿Estás seguro de que deseas eliminar este cronómetro?"):
            self.running = False
            conn = sqlite3.connect('cronometro.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM timer_data WHERE rowid=?', (self.row,))
            conn.commit()
            conn.close()
            self.root.destroy()
            self.app.cronometros.remove(self)

    def on_closing(self):
        self.save_data()
        self.root.destroy()

    def save_data(self):
        conn = sqlite3.connect('cronometro.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS timer_data
                          (elapsed_time REAL, name TEXT)''')
        cursor.execute('DELETE FROM timer_data')
        cursor.execute('INSERT INTO timer_data VALUES (?, ?)', (self.elapsed_time, self.name_entry.get()))
        conn.commit()
        conn.close()

    def load_data(self, name, elapsed_time, row):
        conn = sqlite3.connect('cronometro.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS timer_data
                          (elapsed_time REAL, name TEXT)''')
        cursor.execute('SELECT * FROM timer_data')
        row = cursor.fetchone()
        if row:
            self.elapsed_time, self.name = row
            self.name_entry.insert(0, name)
        conn.close()

class App:
    def __init__(self, root):
        self.root = root
        self.rows = 0  # Comenzamos en 0 para empezar con una fila vacía
        self.cronometros = []  # Lista para almacenar las instancias de Cronometro
        self.init_gui()
        self.load_cronometros_from_db()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        for cronometro in self.cronometros:
            cronometro.save_data()
        self.root.destroy()

    def init_gui(self):
        add_button = tk.Button(self.root, text="Añadir Cronómetro", command=self.add_cronometro)
        add_button.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)

    def add_cronometro(self):
        self.rows += 1
        cronometro_frame = tk.Frame(self.root)
        cronometro_frame.grid(row=self.rows, column=0)
        cronometro = Cronometro(cronometro_frame, self.rows, self)
        self.cronometros.append(cronometro)
    
    def load_cronometros_from_db(self):
        conn = sqlite3.connect('cronometro.db')
        cursor = conn.cursor()
        cursor.execute('SELECT rowid, elapsed_time, name FROM timer_data')
        rows = cursor.fetchall()
        for row in rows:
            rowid, elapsed_time, name = row
            self.rows = max(self.rows, rowid)
            cronometro_frame = tk.Frame(self.root)
            cronometro_frame.grid(row=rowid, column=0)
            cronometro = Cronometro(cronometro_frame, rowid, self, name, elapsed_time)
            self.cronometros.append(cronometro)
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
