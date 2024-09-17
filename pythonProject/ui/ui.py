from prettytable import PrettyTable
import api.api as api
import pandas as pd
import time 
import sys
import matplotlib.pyplot as plt
from time import sleep
import seaborn as sns

def print_letter(text, delay=0.1):
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)
    return ""

def line_feed():
    print("") # Salto de línea

def micro_pause():
    sleep(1)

def line_extendence():
    line_feed()
    print("-" * 90)
    line_feed()

def clean_terminal():
    print("\033[H\033[J")

def get_entry():
    # El programa lee tildes y caracteres especiales, transforma la entrada a mayusculas
    line_feed()
    departamento = input(print_letter("Ingrese el nombre del departamento: ", delay = 0.05)).upper()
    line_feed()
    limit = input(print_letter("Ingrese el limite de datos: ", delay = 0.05))

    try:
        limit = int(limit)
    except ValueError:
        print("El limite debe ser un numero")
        return None, None

    line_feed()
    return departamento, limit

def call_api(departamento, limite):
    # Llamada real a la API
    return api.get_data(limite, departamento)

def get_data(datos):
    # Crear una tabla PrettyTable
    table = PrettyTable()
    table.field_names = datos.columns.tolist()

    for index, row in datos.iterrows():
        table.add_row(row.tolist())

    # Mostrar la tabla en la terminal
    print(table)

def get_number_rows(data):
    micro_pause()
    line_feed()
    print("Number of rows: ", data.shape[0])

def get_number_columns(data):
    micro_pause()
    line_feed()
    print("Number of columns: ", data.shape[1])

def get_column_names(data):
    micro_pause()
    line_feed()
    print("Column Names: ", data.columns.values.tolist())

def get_colum_missing_values(data):
    micro_pause()
    line_feed()
    print("Columns with Missing Values: ", data.columns[data.isnull().any()].tolist())

def get_number_missing_values(data):
    print("Number of rows with Missing Values: ", data.isnull().any(axis=1).sum())

def get_sample_missing_values(data):
    print("Sample Indices with missing data: ", data[data.isnull().any(axis=1)].index.tolist())

def get_dtype(datos):
    micro_pause()
    line_feed()
    table = PrettyTable()
    table.field_names = ["Columna", "Tipo de dato"]
    for columna in datos.columns:
        table.add_row([columna, datos[columna].dtype])
    print(table)

def get_missing_values(datos):
    tabla = PrettyTable()
    tabla.field_names = ["Columna", "Valores faltantes"]
    for columna in datos.columns:
        tabla.add_row([columna, datos[columna].isnull().sum()])
    print(tabla)

def get_sheck_data(data):
    micro_pause()
    print(print_letter("General Stats:", delay=0.1))
    line_feed()
    print(data.info())
    line_feed()
    print(print_letter("Summary Stats:", delay=0.1))
    line_feed()
    print(data.describe())

# Rename columns to lowercase and replace spaces with underscores

def cleanup_column_names(data,rename_dict={},do_inplace=True):
    if not rename_dict:
        return data.rename(columns={col: col.lower().replace(' ','_')
        for col in data.columns.values.tolist()},
        inplace=do_inplace)
    else:
        return data.rename(columns=rename_dict,inplace=do_inplace)
    
# Eliminar columnas con más del 70% de valores nulos

def clean_data_column(data, threshold=0.7):
    return data.dropna(thresh=threshold*data.shape[0], axis=1)

def delete_duplicate_data(data):
    return data.drop_duplicates()

# Gráfica de Barras (para visualizar la frecuencia de categorías como "ciudad_de_ubicación")

def bar_chart(data):
    data['ciudad_de_ubicación'].value_counts().plot(kind='bar')
    plt.title('Frecuencia de Ciudades')
    plt.xlabel('Ciudad de Ubicación')
    plt.ylabel('Frecuencia')
    plt.show()

# Gráfica de Pastel (Pie Chart) (para visualizar proporciones de "ciudad_de_ubicación"):

def pie_chart(data):
    data['ciudad_de_ubicación'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, shadow=False)
    plt.title('Proporción de Ciudades')
    plt.axis('equal')
    plt.show()

# Histograma (para visualizar la distribución de "edad")

def convert_to_int(data):
    data['edad'] = data['edad'].astype(int)

def histogram(data):
    data['edad'].plot(kind='hist', bins=20)
    plt.title('Distribución de Edad')
    plt.xlabel('Edad')
    plt.ylabel('Frecuencia')
    plt.show()

# Heatmap de Frecuencia (para ver la relación entre "ciudad_de_ubicación" y "tipo" utilizando seaborn)

def heatmap(data):
    pivot_table = data.pivot_table(index='ciudad_de_ubicación', columns='tipo', aggfunc='size', fill_value=0)
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, cmap='Blues')
    plt.title('Mapa de Calor: Ciudad de Ubicación vs Tipo')
    plt.show()

# Boxplot (Gráfica de Cajas y Bigotes) (para visualizar la distribución de "edad" y detectar outliers):

def boxplot(data):
    sns.boxplot(x=data['edad'])
    plt.title('Distribución de Edad')
    plt.show()


def menu():
    table = PrettyTable()
    table.field_names = ["Option", "Description"]
    table.add_row([1, "Bar Chart"])
    table.add_row([2, "Pie Chart"])
    table.add_row([3, "Histogram"])
    table.add_row([4, "Heatmap"])
    table.add_row([5, "Boxplot"])
    table.add_row([6, "Exit"])
    print(table)

def data_visualization(data):
    while True:
        clean_terminal()
        menu()
        option = input("Enter an option: ")

        if option == '1':
            bar_chart(data)
        elif option == '2':
            pie_chart(data)
        elif option == '3':
            histogram(data)
        elif option == '4':
            heatmap(data)
        elif option == '5':
            boxplot(data)
        elif option == '6':
            print_letter("Goodbye!", delay=0.1)
            break
        else:
            print("Invalid option")


def understanding_data(data):
    get_number_rows(data)
    get_number_columns(data)
    get_column_names(data)
    get_dtype(data)
    line_feed()
    get_colum_missing_values(data)
    get_missing_values(data)
    get_number_missing_values(data)
    get_sample_missing_values(data)
    line_extendence()
    get_sheck_data(data)
    line_feed()
    line_extendence()


# import api.api as api
# from prettytable import PrettyTable
# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button 
# from kivy.core.window import Window 

# class MyGridLayout(GridLayout): # Clase para el layout de la aplicación
#     def __init__(self, **kwargs): # Constructor de la clase
#         super(MyGridLayout, self).__init__(**kwargs) # Llamar al constructor de la clase base
#         self.cols = 2

#         # Add widgets
#         self.add_widget(Label(text="Filtrar por departamento:"))
#         self.departamento = TextInput(multiline=False) # No permitir saltos de línea
#         self.add_widget(self.departamento) # Añadir el widget al layout

#         self.add_widget(Label(text="Limite de datos:"))
#         self.limite = TextInput(multiline=False)
#         self.add_widget(self.limite)

#         self.submit = Button(text="Submit")
#         self.submit.bind(on_press=self.on_submit)
#         self.add_widget(self.submit)

#     def on_submit(self, instance):
#         departamento = self.departamento.text.upper()
#         limite = self.limite.text

#         try:
#             limite = int(limite)
#         except ValueError:
#             print("El limite debe ser un numero")
#             return

#         datos = api.get_data(limite, departamento)
#         self.mostrar_datos(datos)
#         App.get_running_app().stop()  # Cerrar la aplicación Kivy
#         Window.close()  # Cerrar la ventana de Kivy

#     def mostrar_datos(self, datos):
#         if datos.empty:
#             print("No se encontraron datos")
#             return

#         # Crear una tabla PrettyTable
#         table = PrettyTable()
#         table.field_names = datos.columns.tolist()

#         for index, row in datos.iterrows():
#             table.add_row(row.tolist())

#         # Mostrar la tabla en la consola
#         print(table)

# class MyApp(App):
#     def build(self):
#         Window.size = (400, 150)  # Ajustar el tamaño de la ventana
#         return MyGridLayout()

# if __name__ == '__main__':
#     MyApp().run()