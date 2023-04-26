import tkinter as tk
from tkinter import filedialog
import pandas as pd
import PySimpleGUI as sg

# Define la ventana emergente
layout = [[sg.Text('Ingresa la nota:'), sg.InputText()],[sg.Button('Ok')]]

# Crea la ventana
window = sg.Window('Ingresar nota', layout)

# Loop para leer los eventos y datos de entrada
while True:
    event, values = window.read()
    if event == 'Ok':
        nota = values[0]
        break

# Cierra la ventana
window.close()

# Imprime la nota ingresada
print("Ultima nota:", nota)


order_path = filedialog.askopenfilename(title="Selecciona 'Orden Cliente'", filetypes=(("Archivo de Excel", "*.xlsx"),))
master_path = filedialog.askopenfilename(title="Selecciona Maestro de clientes", filetypes=(("Archivo de Excel", "*.xlsx"),))

