import sqlite3
import datetime

import sqlite3

def eliminar_cita_fecha(fecha_eliminar):
  """Deletes an appointment from 'ximenadoctora.db' based on the provided date.

  Args:
      fecha_eliminar (str): The date of the appointment to be deleted in YYYY-MM-DD format.

  Returns:
      None
  """

  try:
    with sqlite3.connect('ximenadoctora.db') as conn:
      cursor = conn.cursor()

      # Use a parameterized query to prevent SQL injection vulnerabilities
      cursor.execute("""
        DELETE FROM Cita WHERE FechaCita = ?
      """, (fecha_eliminar,))

      conn.commit()
      print("Cita eliminada exitosamente.")  # Informative message

  except sqlite3.Error as e:
    print("Error al intentar eliminar la cita:", e)
  except Exception as ex:
    print(f"Error inesperado: {ex}")


def eliminar_cita_folio(folio_cita):
    try:
        with sqlite3.connect('ximenadoctora.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM Cita
                WHERE FolioCita = ?
            """, (folio_cita,))
            conn.commit()   
            print(f"La cita con folio {folio_cita} ha sido eliminada correctamente.")
    except sqlite3.Error as e:
        print("Error al eliminar la cita:", e)
