import sqlite3
import pandas as pd
import numpy as np

def estadisticos_genero(genero):
    try:
        # Establecer conexión a la base de datos
        with sqlite3.connect("ximenadoctora.db") as conexion:
            # Leer los datos de las tablas y cargarlos en DataFrames
            df_paciente = pd.read_sql_query("SELECT * FROM Paciente", conexion)
            df_cita = pd.read_sql_query("SELECT * FROM Cita", conexion)
            df_asistencia_cita = pd.read_sql_query("SELECT * FROM AsistenciaCita", conexion)
            
            # Combinar los DataFrames según las claves
            df_merged = pd.merge(df_paciente, df_cita, left_on='ClavePaciente', right_on='ClavePaciente')
            df_merged = pd.merge(df_merged, df_asistencia_cita, left_on='FolioCita', right_on='FolioCita')
            
            # Filtrar por género
            df_genero = df_merged[df_merged['Sexo'] == genero]
            
            # Calcular estadísticas
            estadisticas = {}
            for columna in ['Edad', 'Peso', 'Estatura', 'PresionSistolica', 'PresionDiastolica']:
                datos = df_genero[columna]
                estadisticas[columna] = {
                    'conteo': datos.count(),
                    'minimo': datos.min(),
                    'maximo': datos.max(),
                    'media': np.mean(datos),
                    'mediana': np.median(datos),
                    'desviacion_estandar': np.std(datos)
                }
            
            # Convertir el diccionario de estadísticas en DataFrame
            df_estadisticas = pd.DataFrame(estadisticas)
            
            return estadisticas, df_estadisticas
            
    except sqlite3.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None, None

def estadisticos_genero_edad(genero, rango_edad):
    try:
        # Establecer conexión a la base de datos
        with sqlite3.connect("ximenadoctora.db") as conexion:
            # Leer los datos de las tablas y cargarlos en DataFrames
            df_paciente = pd.read_sql_query("SELECT * FROM Paciente", conexion)
            df_cita = pd.read_sql_query("SELECT * FROM Cita", conexion)
            df_asistencia_cita = pd.read_sql_query("SELECT * FROM AsistenciaCita", conexion)
            
            # Combinar los DataFrames según las claves
            df_merged = pd.merge(df_paciente, df_cita, left_on='ClavePaciente', right_on='ClavePaciente')
            df_merged = pd.merge(df_merged, df_asistencia_cita, left_on='FolioCita', right_on='FolioCita')
            
            # Filtrar por género
            df_genero = df_merged[df_merged['Sexo'] == genero]
            
            # Filtrar por rango de edad
            df_edad = df_genero[(df_genero['Edad'] >= rango_edad[0]) & (df_genero['Edad'] <= rango_edad[1])]
            
            # Calcular estadísticas
            estadisticas = {}
            for columna in ['Edad', 'Peso', 'Estatura', 'PresionSistolica', 'PresionDiastolica']:
                datos = df_edad[columna]
                estadisticas[columna] = {
                    'conteo': datos.count(),
                    'minimo': datos.min(),
                    'maximo': datos.max(),
                    'media': np.mean(datos),
                    'mediana': np.median(datos),
                    'desviacion_estandar': np.std(datos)
                }
            
            return estadisticas
    except sqlite3.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def estadisticos_edad(inicio, fin):
    try:
        # Establecer conexión a la base de datos
        with sqlite3.connect("ximenadoctora.db") as conexion:
            # Leer los datos de las tablas y cargarlos en DataFrames
            df_paciente = pd.read_sql_query("SELECT * FROM Paciente", conexion)
            df_cita = pd.read_sql_query("SELECT * FROM Cita", conexion)
            df_asistencia_cita = pd.read_sql_query("SELECT * FROM AsistenciaCita", conexion)
            
            # Combinar los DataFrames según las claves
            df_merged = pd.merge(df_paciente, df_cita, left_on='ClavePaciente', right_on='ClavePaciente')
            df_merged = pd.merge(df_merged, df_asistencia_cita, left_on='FolioCita', right_on='FolioCita')
            
            # Filtrar por rango de edad
            df_edad = df_merged[(df_merged['Edad'] >= inicio) & (df_merged['Edad'] <= fin)]
            
            # Calcular estadísticas
            estadisticas = {}
            for columna in ['Edad', 'Peso', 'Estatura', 'PresionSistolica', 'PresionDiastolica']:
                datos = df_edad[columna]
                estadisticas[columna] = {
                    'conteo': datos.count(),
                    'minimo': datos.min(),
                    'maximo': datos.max(),
                    'media': np.mean(datos),
                    'mediana': np.median(datos),
                    'desviacion_estandar': np.std(datos)
                }
            
            # Convertir el diccionario de estadísticas en DataFrame
            df_estadisticas = pd.DataFrame(estadisticas)
            
            return estadisticas, df_estadisticas
            
    except sqlite3.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None, None

import pandas as pd
from openpyxl import Workbook

def dataframe_csv(data, filename):
    try:
        if isinstance(data, pd.DataFrame):
            data.to_csv(filename, index=False)
            print(f"Se ha guardado el DataFrame en {filename}")
        else:
            # Intenta convertir el valor a DataFrame
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            print(f"Se ha guardado el valor en CSV en {filename}")
    except Exception as e:
        print(f"Error al guardar en CSV: {e}")

def dataframe_excel(data, filename):
    try:
        if isinstance(data, pd.DataFrame):
            data.to_excel(filename, index=False)
            print(f"Se ha guardado el DataFrame en {filename}")
        else:
            # Intenta convertir el valor a DataFrame
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False)
            print(f"Se ha guardado el valor en Excel en {filename}")
    except Exception as e:
        print(f"Error al guardar en Excel: {e}")



