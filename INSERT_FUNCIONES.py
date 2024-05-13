import sys
import sqlite3
from sqlite3 import Error

def registrar_pacientes(primerapellido, segundoapellido, nombre, fechanacimiento, sexo, edad):
    try:
        with sqlite3.connect("ximenadoctora.db") as conn:
            mi_cursor = conn.cursor()
            valores =(primerapellido, segundoapellido, nombre, fechanacimiento, sexo, edad)
            mi_cursor.execute("INSERT INTO Paciente (PrimerApellido, SegundoApellido, Nombre, FechaNacimiento, Sexo, edad) VALUES (?, ?, ?, ?, ?, ?)", valores)
            print("Registros del paciente agregados. ID del paciente:", mi_cursor.lastrowid)
    except sqlite3.Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

def registrar_citas(clavepaciente, fechacita, turnocita):
    try:
        with sqlite3.connect("ximenadoctora.db") as conn:
            mi_cursor = conn.cursor()
            valores =(clavepaciente, fechacita, turnocita)
            mi_cursor.execute("INSERT INTO Cita (ClavePaciente, FechaCita, TurnoCita) VALUES(?,?,?)", valores)
            print("Registros de la cita agregados")
    except sqlite3.Error as e:
        print (e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

def citas_realizadas(foliocita, clavepaciente, horallegada, peso, estatura, presionsistolica, presiondiastolica, diagnostico):
    try:
        with sqlite3.connect("ximenadoctora.db") as conn:
            mi_cursor = conn.cursor()
            valores = (foliocita, clavepaciente, horallegada, peso, estatura, presionsistolica, presiondiastolica, diagnostico)
            mi_cursor.execute("INSERT INTO AsistenciaCita (FolioCita, ClavePaciente, HoraLlegada, Peso, Estatura, PresionSistolica, PresionDiastolica, Diagnostico) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", valores)
            print("Registros de la asistencia de la cita agregados")
    except sqlite3.Error as e:
        print("Error al insertar datos:", e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

import sqlite3

def insertar_tiposexo(tipo, descripcion):
    try:
        with sqlite3.connect('ximenadoctora.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO TipoSexo (idtipo, Tipo, Descripcion) VALUES (NULL, ?, ?)", (tipo, descripcion))
            conn.commit()
        return True
    except sqlite3.Error as e:
        print("Error al insertar en la tabla TipoSexo:", e)
        return False


