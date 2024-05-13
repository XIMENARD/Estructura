import sys
import sqlite3
from sqlite3 import Error
from datetime import datetime as datetime
from datetime import date


def consultar_clavepaciente_cita(clavepaciente):
    try:
        with sqlite3.connect("ximenadoctora.db") as conn:
            mi_cursor = conn.cursor()
            consulta = 'SELECT * FROM Cita WHERE ClavePaciente = ?'
            mi_cursor.execute(consulta, (clavepaciente,))
            consulta_resultado = mi_cursor.fetchone()
            return consulta_resultado
    except sqlite3.Error as e:
        print(e)
    except Exception as ex:
        print(f"Se produjo el siguiente error: {ex}")

def consultar_clavepaciente_cita_maquina():
    try:
        with sqlite3.connect("ximenadoctora.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute('SELECT ClavePaciente FROM Cita')
            claves_pacientes = mi_cursor.fetchall()
            print("Claves de los pacientes:")
            for clave in claves_pacientes:
                print(clave[0])
    except sqlite3.Error as e:
        print(e)
    except Exception as ex:
        print(f"Se produjo el siguiente error: {ex}")

def consultar_clavepaciente_paciente(clavepaciente):
    try:
        with sqlite3.connect("ximenadoctora.db") as conn:
            mi_cursor = conn.cursor()
            consulta = 'SELECT * FROM Paciente WHERE ClavePaciente = ?'
            mi_cursor.execute(consulta, (clavepaciente,))
            consulta_resultado = mi_cursor.fetchone()
            return consulta_resultado
    except sqlite3.Error as e:
        print(e)
    except Exception as ex:
        print(f"Se produjo el siguiente error: {ex}")

def consultar_clavepaciente_paciente_maquina():
    try:
        with sqlite3.connect("ximenadoctora.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute('SELECT ClavePaciente FROM Paciente')
            claves_pacientes = mi_cursor.fetchall()
            print("Claves de los pacientes:")
            for clave in claves_pacientes:
                print(clave[0])
    except sqlite3.Error as e:
        print(e)
    except Exception as ex:
        print(f"Se produjo el siguiente error: {ex}")

def consultar_fechacita_asistenciacita(fecha):
    """
    Retrieves patient names and appointment slots for a given date,
    formatting patient names with spaces instead of commas.

    Args:
        fecha (date): The date for which to retrieve appointment information.

    Returns:
        list: A list of tuples containing formatted patient names and appointment slots
              (if there are multiple appointments) or None (if no appointments found).
    """

    try:
        with sqlite3.connect('ximenadoctora.db') as conn:
            cursor = conn.cursor()
            fecha_actual = date.today()

            # Convert dates to strings in YYYY-MM-DD format before using in query
            fecha_str = fecha.strftime('%Y-%m-%d')
            fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')

            query = """
                SELECT Paciente.PrimerApellido || ' ' || Paciente.SegundoApellido || ' ' || Paciente.Nombre AS NombreCompleto,
                       Cita.TurnoCita AS Turno
                FROM Cita
                INNER JOIN Paciente ON Cita.ClavePaciente = Paciente.ClavePaciente
                WHERE Cita.FechaCita = ? AND Cita.FechaCita >= ?;
            """
            cursor.execute(query, (fecha_str, fecha_actual_str))

            results = cursor.fetchall()

            if results:
                # Modify the name formatting (same as before)
                formatted_results = []
                for fila in results:
                    nombre_completo = fila[0].split(', ')
                    nombre_espacios = ' '.join(nombre_completo)
                    formatted_results.append((nombre_espacios, fila[1]))
                return formatted_results
            else:
                return None  # No appointments found

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

    finally:
        # Ensure connection is closed even if exceptions occur
        conn.close()

def consulta_pacientespendientes_citas():
    try:
        with sqlite3.connect('ximenadoctora.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Paciente.ClavePaciente, Paciente.PrimerApellido, Paciente.SegundoApellido, Paciente.Nombre, Cita.FolioCita
                FROM Paciente
                INNER JOIN Cita ON Paciente.ClavePaciente = Cita.ClavePaciente
                WHERE Cita.FechaCita >= DATE('now')
                ORDER BY Paciente.PrimerApellido, Paciente.SegundoApellido, Paciente.Nombre
            """)
            consulta = cursor.fetchall()
            
            return consulta
    
    except sqlite3.Error as e:
        print("Error al realizar la consulta:", e)
        return None

def obtener_citas_futuras_por_paciente(folio_paciente):
    try:
        with sqlite3.connect('ximenadoctora.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT FolioCita, FechaCita, TurnoCita
                FROM Cita
                WHERE ClavePaciente = ? AND FechaCita >= DATE('now')
                ORDER BY FechaCita, TurnoCita
            """, (folio_paciente,))
            
            citas_paciente = cursor.fetchall()

            return citas_paciente
    
    except sqlite3.Error as e:
        print("Error al realizar la consulta:", e)
        return None