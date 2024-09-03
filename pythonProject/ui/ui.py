# from prettytable import PrettyTable
# import api.api as api

# def obtener_entrada():
#     #el programa lee tildes y caracteres especiales, transforma la entrada a mayusculas
#     departamento = input("Filtrar por departamento: ").upper()
#     limite = input("Limite de datos: ")

#     try:
#         limite = int(limite)
#     except ValueError:
#         print("El limite debe ser un numero")
#         return None, None

#     return departamento, limite

# def llamar_api(departamento, limite):
#     # Llamada real a la API
#     return api.get_data(limite, departamento)

# def mostrar_datos(datos):
#     # Crear una tabla PrettyTable
#     table = PrettyTable()
#     table.field_names = datos.columns.tolist()

#     for index, row in datos.iterrows():
#         table.add_row(row.tolist())

#     # Mostrar la tabla en la terminal
#     print(table)

# def main():
#     departamento, limite = obtener_entrada()
#     if departamento is not None and limite is not None:
#         datos = llamar_api(departamento, limite)
#         mostrar_datos(datos)

# if __name__ == '__main__':
#     main()

import api.api as api
from prettytable import PrettyTable
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button 
from kivy.core.window import Window 

class MyGridLayout(GridLayout): # Clase para el layout de la aplicación
    def __init__(self, **kwargs): # Constructor de la clase
        super(MyGridLayout, self).__init__(**kwargs) # Llamar al constructor de la clase base
        self.cols = 2

        # Add widgets
        self.add_widget(Label(text="Filtrar por departamento:"))
        self.departamento = TextInput(multiline=False) # No permitir saltos de línea
        self.add_widget(self.departamento) # Añadir el widget al layout

        self.add_widget(Label(text="Limite de datos:"))
        self.limite = TextInput(multiline=False)
        self.add_widget(self.limite)

        self.submit = Button(text="Submit")
        self.submit.bind(on_press=self.on_submit)
        self.add_widget(self.submit)

    def on_submit(self, instance):
        departamento = self.departamento.text.upper()
        limite = self.limite.text

        try:
            limite = int(limite)
        except ValueError:
            print("El limite debe ser un numero")
            return

        datos = api.get_data(limite, departamento)
        self.mostrar_datos(datos)
        App.get_running_app().stop()  # Cerrar la aplicación Kivy
        Window.close()  # Cerrar la ventana de Kivy

    def mostrar_datos(self, datos):
        if datos.empty:
            print("No se encontraron datos")
            return

        # Crear una tabla PrettyTable
        table = PrettyTable()
        table.field_names = datos.columns.tolist()

        for index, row in datos.iterrows():
            table.add_row(row.tolist())

        # Mostrar la tabla en la consola
        print(table)

class MyApp(App):
    def build(self):
        Window.size = (400, 150)  # Ajustar el tamaño de la ventana
        return MyGridLayout()

if __name__ == '__main__':
    MyApp().run()