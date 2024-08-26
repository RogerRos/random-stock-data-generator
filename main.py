import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Función para obtener el siguiente número de archivo
def get_next_file_number(folder):
    existing_files = [int(f.split('.')[0]) for f in os.listdir(folder) if f.endswith('.csv') and f.split('.')[0].isdigit()]
    if existing_files:
        return max(existing_files) + 1
    else:
        return 1

# Función que se ejecuta al hacer clic en el botón "Order"
def generate_files():
    try:
        num_days = int(entry_days.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce un número válido de días.")
        return
    
    records_per_day = 390  # Registros por día
    csv_folder = "data/csv_files"
    os.makedirs(csv_folder, exist_ok=True)
    start_file_number = get_next_file_number(csv_folder)

    for day in range(num_days):
        num_rows = records_per_day
        start_time = datetime(2023, 8, 26, 9, 0, 0) + timedelta(days=day)
        time_delta = timedelta(seconds=1)
        
        timestamps = [start_time + i * time_delta for i in range(num_rows)]
        bids = np.round(np.random.normal(1.1010, 0.0002, num_rows), 4)
        asks = np.round(bids + np.random.normal(0.0002, 0.0001, num_rows), 4)
        
        df = pd.DataFrame({
            "timestamp": timestamps,
            "bid": bids,
            "ask": asks
        })
        
        filename = f"{start_file_number + day}.csv"
        df.to_csv(os.path.join(csv_folder, filename), index=False)
    
    messagebox.showinfo("execution done", f"Generated {num_days} CSV files in folder '{csv_folder}'.")

# Función para centrar la ventana en la pantalla
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

# Configuración de la ventana principal de tkinter
root = tk.Tk()
root.title("ROS stock CSV data generator")

# Ajustar el tamaño de la ventana
window_width = 400
window_height = 200
center_window(root, window_width, window_height)

# Etiqueta y campo de entrada para los días
label_days = tk.Label(root, text="Days to generate:")
label_days.pack(pady=10)

entry_days = tk.Entry(root, width=30)
entry_days.pack(pady=5)

# Botón "Order"
button_order = tk.Button(root, text="Order", command=generate_files)
button_order.pack(pady=20)

# Iniciar la interfaz
root.mainloop()
