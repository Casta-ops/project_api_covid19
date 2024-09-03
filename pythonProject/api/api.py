import pandas as pd
from sodapy import Socrata
import requests

def get_data(limite, departamento_nom):
    client = Socrata("www.datos.gov.co", None)

    try:
        # Ajustar la llamada a la API para filtrar por departamento y limitar los resultados
        query = f"departamento_nom='{departamento_nom}'" # Filtro por departamento
        results = client.get("gt2j-8ykr", where=query, limit=limite) # Limitar los resultados
    except requests.exceptions.RequestException as e: # Capturar errores de conexión
        print(f"Error al conectar con la API: {e}") # Imprimir el error
        return pd.DataFrame()  # Retornar un DataFrame vacío en caso de error

    # Convertir los resultados a un DataFrame
    df = pd.DataFrame.from_records(results)

    # Seleccionar solo las columnas necesarias
    columnas_necesarias = [
        "ciudad_municipio_nom", "departamento_nom", "edad", 
        "fuente_tipo_contagio", "estado", "pais_viajo_1_nom"
    ]

    # Verificar si las columnas necesarias están presentes, si no, agregarlas con valores predeterminados
    for columna in columnas_necesarias:
        if columna not in df.columns:
            df[columna] = None

    df = df[columnas_necesarias]

    # Renombrar las columnas para que sean más legibles
    df.columns = [
        "Ciudad de ubicación", "Departamento", "Edad", 
        "Tipo", "Estado", "País de procedencia"
    ]

    return df

def get_departamentos():
    client = Socrata("www.datos.gov.co", None)

    try:
        results = client.get("gt2j-8ykr", select="distinct departamento_nom")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return pd.DataFrame()  # Retornar un DataFrame vacío en caso de error

    return pd.DataFrame.from_records(results)