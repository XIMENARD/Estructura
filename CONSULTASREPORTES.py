import sqlite3
import pandas as pd

def obtener_citas_periodo(fecha_inicio, fecha_fin):
    consulta = """
    SELECT 
        Paciente.PrimerApellido, 
        Paciente.SegundoApellido, 
        Paciente.Nombre, 
        Cita.FechaCita, 
        AsistenciaCita.PresionSistolica, 
        AsistenciaCita.PresionDiastolica, 
        Paciente.Edad
    FROM 
        Paciente
    JOIN 
        Cita ON Paciente.ClavePaciente = Cita.ClavePaciente
    LEFT JOIN 
        AsistenciaCita ON Cita.FolioCita = AsistenciaCita.FolioCita
    WHERE 
        Cita.FechaCita BETWEEN ? AND ?
    ORDER BY 
        Paciente.PrimerApellido, 
        Paciente.SegundoApellido, 
        Paciente.Nombre, 
        Cita.FechaCita
    """

    with sqlite3.connect('ximenadoctora.db') as conn:
        df = pd.read_sql_query(consulta, conn, params=(fecha_inicio, fecha_fin))

    return df

def obtener_citas_paciente(clave_paciente):
    consulta = """
    SELECT 
        Paciente.PrimerApellido, 
        Paciente.SegundoApellido, 
        Paciente.Nombre, 
        Cita.FechaCita, 
        AsistenciaCita.PresionSistolica, 
        AsistenciaCita.PresionDiastolica, 
        Paciente.Edad
    FROM 
        Paciente
    JOIN 
        Cita ON Paciente.ClavePaciente = Cita.ClavePaciente
    LEFT JOIN 
        AsistenciaCita ON Cita.FolioCita = AsistenciaCita.FolioCita
    WHERE 
        Paciente.ClavePaciente = ?
    ORDER BY 
        Cita.FechaCita
    """

    with sqlite3.connect('ximenadoctora.db') as conn:
        df = pd.read_sql_query(consulta, conn, params=(clave_paciente,))

    return df

def consulta_pacientes_completo():

    with sqlite3.connect('ximenadoctora.db') as conn:
        consulta = "SELECT * FROM Paciente;"
        pacientes_df = pd.read_sql_query(consulta, conn)
        if not pacientes_df.empty:
            print(pacientes_df)
            return pacientes_df
        else:
            print("No hay pacientes en la base de datos.")


def buscar_paciente_clave(clave):
    with sqlite3.connect('ximenadoctora.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Paciente WHERE ClavePaciente = ?", (clave,))
        paciente = cursor.fetchone()
        
        if paciente:
            paciente_dict = {
                'ClavePaciente': paciente[0],
                'PrimerApellido': paciente[1],
                'SegundoApellido': paciente[2],
                'Nombre': paciente[3],
                'FechaNacimiento': paciente[4],
                'Sexo': paciente[5]
            }
            paciente_df = pd.DataFrame([paciente_dict])
            consulta_expediente = input("¿Desea consultar el expediente clínico? (s/n): ")
            if consulta_expediente.lower() == 's':
                expediente_df = consultar_expediente_clinico(clave)
                if not expediente_df.empty:
                    paciente_df = pd.merge(paciente_df, expediente_df, on='ClavePaciente', how='left')
        else:
            print("No se encontró ningún paciente con la clave especificada.")
            paciente_df = pd.DataFrame()
        return paciente_df


def buscar_paciente_nombreapellidos(nombre, primer_apellido, segundo_apellido=None):
    with sqlite3.connect('ximenadoctora.db') as conn:
        cursor = conn.cursor()
        if segundo_apellido:
            cursor.execute("SELECT * FROM Paciente WHERE Nombre = ? AND PrimerApellido = ? AND SegundoApellido = ?", 
                           (nombre, primer_apellido, segundo_apellido))
        else:
            cursor.execute("SELECT * FROM Paciente WHERE Nombre = ? AND PrimerApellido = ?", 
                           (nombre, primer_apellido))
        paciente = cursor.fetchone()
        
        if paciente:
            paciente_dict = {
                'ClavePaciente': paciente[0],
                'PrimerApellido': paciente[1],
                'SegundoApellido': paciente[2],
                'Nombre': paciente[3],
                'FechaNacimiento': paciente[4],
                'Sexo': paciente[5]
            }
            paciente_df = pd.DataFrame([paciente_dict])
            consulta_expediente = input("¿Desea consultar el expediente clínico? (s/n): ")
            if consulta_expediente.lower() == 's':
                expediente_df = consultar_expediente_clinico(paciente[0])
                if not expediente_df.empty:
                    paciente_df = pd.merge(paciente_df, expediente_df, on='ClavePaciente', how='left')
        else:
            print("No se encontró ningún paciente con los nombres y apellidos especificados.")
            paciente_df = pd.DataFrame()
        return paciente_df


def consultar_expediente_clinico(clave):
    with sqlite3.connect('ximenadoctora.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Cita WHERE ClavePaciente = ?", (clave,))
        citas = cursor.fetchall()
        
        if citas:
            print("Expediente clínico del paciente:")
            for cita in citas:
                print("Fecha de la cita:", cita[2])
                print("Turno de la cita:", cita[3])
                cursor.execute("SELECT HoraLlegada, Diagnostico FROM AsistenciaCita WHERE FolioCita = ?", (cita[0],))
                asistencia = cursor.fetchone()
                if asistencia:
                    print("Hora de llegada:", asistencia[0])
                    print("Diagnóstico:", asistencia[1])
                else:
                    print("No se registró la asistencia a esta cita.")
                print("---------------------------------")
        else:
            print("El paciente no tiene citas registradas en su expediente clínico.")

