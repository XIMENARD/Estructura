import pandas as pd
import sys
import re
import statistics
import sqlite3
from sqlite3 import Error as e
import datetime as datetime
from datetime import datetime, timedelta
from INSERT_FUNCIONES import registrar_pacientes, registrar_citas, citas_realizadas 
import openpyxl


generos = ['H', 'M', 'N']
tipocita = ['1','2','3']
tipocita = {
    "1": "mañana",
    "2": "mediodia",
    "3": "tarde"
}

try:
    with sqlite3.connect('ximenadoctora.db') as conn:
        cursor_ximena = conn.cursor()

        tabla_paciente = """
        CREATE TABLE IF NOT EXISTS Paciente (
            ClavePaciente INTEGER PRIMARY KEY AUTOINCREMENT,
            PrimerApellido TEXT,
            SegundoApellido TEXT,
            Nombre TEXT,
            FechaNacimiento DATE,
            Sexo TEXT,
            Edad INTEGER
        );
        """

        tabla_cita = """
        CREATE TABLE IF NOT EXISTS Cita (
            FolioCita INTEGER PRIMARY KEY AUTOINCREMENT,
            ClavePaciente INTEGER,
            FechaCita DATE,
            TurnoCita INTEGER,
            FOREIGN KEY (ClavePaciente) REFERENCES Paciente(ClavePaciente)
        );
        """


        tabla_asistencia_cita = """
        CREATE TABLE IF NOT EXISTS AsistenciaCita (
            FolioAsistencia INTEGER PRIMARY KEY AUTOINCREMENT,
            FolioCita INTEGER,
            ClavePaciente INTEGER,
            HoraLlegada TIME,
            Peso REAL,
            Estatura REAL,
            PresionSistolica INTEGER,
            PresionDiastolica INTEGER,
            Diagnostico TEXT,
            FOREIGN KEY (FolioCita) REFERENCES Cita(FolioCita),
            FOREIGN KEY (ClavePaciente) REFERENCES Paciente(ClavePaciente)
        );
        """

        cursor_ximena.execute(tabla_paciente)
        cursor_ximena.execute(tabla_cita)
        cursor_ximena.execute(tabla_asistencia_cita)

        print("Tablas creadas exitosamente.")

except sqlite3.Error as e:
    print("Error al trabajar con la base de datos SQLite:", e)

def validador_fechas(fecha):
    try:
        datetime.strptime(fecha, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def reporte_citas_menu():
    opciones_reporte_citas = ['1', '2', '3']
    while True:
        print('Submenu de REORTES DE CITAS eliga la opcion que desea\n[1]Por periodo\n[2]Por paciente\n[3]Regresar al menu de consultas y reportes')
        opcion = input('R: ')
        if opcion == '':
            print('NO SE DEBE OMITIR EL DATO')
            continue
        if opcion not in opciones_reporte_citas:
            print('OPCION INVALIDA SOLO SE PUEDEN SELECCIONAR DEL 1 AL 3')
            continue

        if opcion == '1':
            while True:
                fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
                fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
                
                if not fecha_inicio or not fecha_fin:
                    print("Debe ingresar ambas fechas. Intente nuevamente.")
                    continue
                
                try:
                    pd.to_datetime(fecha_inicio)
                    pd.to_datetime(fecha_fin)
                except ValueError:
                    print("Formato de fecha inválido. Intente nuevamente.")
                    continue

                if fecha_fin >= fecha_inicio:
                    from CONSULTASREPORTES import obtener_citas_periodo
                    df_por_periodo = obtener_citas_periodo(fecha_inicio, fecha_fin)
                    print("Citas por período:")
                    print(df_por_periodo)
                    while True:
                        from ESTADISTICA import dataframe_csv, dataframe_excel
                        print("1. Guardar en CSV")
                        print("2. Guardar en Excel")
                        print("3. Salir")

                        opcion = input("Ingrese su opción: ")

                        if opcion == '1':
                            df_por_periodo.to_csv('datosCitaporperiodo.csv', index=False)
                            break
                        elif opcion == '2':
                            df_por_periodo.to_excel('datosCitaporperiodo.xlsx', index=False)
                            break
                        elif opcion == '3':
                            print("Saliendo del programa...")
                            break
                        else:
                            print("Opción no válida")
                        break
                else:
                    print("La fecha de fin debe ser posterior o igual a la fecha de inicio. Intente nuevamente.")

        if opcion == '2':
            while True:
                clave_paciente = input("Ingresa el ID del paciente deseado (en formato str): ")
                
                if clave_paciente.strip() == "":
                    print("¡Por favor, ingresa un valor para la clave del paciente!")
                    continue
                
                if not clave_paciente.isdigit():
                    print("¡El ID del paciente debe ser un número!")
                    continue
                from CONSULTASREPORTES import obtener_citas_paciente
                clave_paciente = int(clave_paciente)
                df_por_paciente = obtener_citas_paciente(clave_paciente)
                print("\nCitas por paciente:")
                print(df_por_paciente)
                while True:
                    from ESTADISTICA import dataframe_csv, dataframe_excel
                    print("1. Guardar en CSV")
                    print("2. Guardar en Excel")
                    print("3. Salir")

                    opcion = input("Ingrese su opción: ")

                    if opcion == '1':
                        df_por_paciente.to_csv('datosCitaporpaciente.csv', index=False)
                        break
                    elif opcion == '2':
                        df_por_paciente.to_excel('datosCitaporpaciente.xlsx', index=False)
                        break
                    elif opcion == '3':
                        print("Saliendo del programa...")
                        break
                    else:
                        print("Opción no válida")
                break
       
        if opcion == '3':
           break

def reportes_pacientes_menu():
   opciones_reportes_pacientes_menu = ['1', '2', '3', '4']
   while True:
        print('Submenu de REPORTES DE PACIENTES eliga la opcion que desea\n[1]Listado completo de pacientes\n[2]Busqueda por clave de pacientes\n[3]Busqueda por apellido y nombres\n[4]Regresar al menu de consultas y reportes')
        opcion = input('R: ')
        if opcion == '':
            print('NO SE DEBE OMITIR EL DATO')
            continue
        if opcion not in opciones_reportes_pacientes_menu:
            print('OPCION INVALIDA SOLO SE PUEDEN SELECCIONAR DEL 1 AL 4')
            continue

        if opcion == '1':
            from CONSULTASREPORTES import consulta_pacientes_completo
            df_pacientescompleto = consulta_pacientes_completo()
            while True:
                from ESTADISTICA import dataframe_csv, dataframe_excel
                print("1. Guardar en CSV")
                print("2. Guardar en Excel")
                print("3. Salir")

                opcion = input("Ingrese su opción: ")

                if opcion == '1':
                    df_pacientescompleto.to_csv('pacientes.csv', index=False)
                    break
                elif opcion == '2':
                    df_pacientescompleto.to_excel('pacientes.xlsx', index=False)
                    break
                elif opcion == '3':
                    print("Saliendo del programa...")
                    break
                else:
                    print("Opción no válida")

        if opcion == '2':
            while True:
                from CONSULTASREPORTES import buscar_paciente_clave
                clave_paciente = input("Por favor, ingrese la clave del paciente a consultar (solo números): ").strip()
                if not clave_paciente:
                    print("No se ha ingresado ningún valor. Por favor, ingrese la clave del paciente.")
                    continue
                if not clave_paciente.isdigit():
                    print("Por favor, ingrese solo números.")
                    continue
                df_pacientesclave = buscar_paciente_clave(clave_paciente)
                while True:
                    from ESTADISTICA import dataframe_csv, dataframe_excel
                    print("1. Guardar en CSV")
                    print("2. Guardar en Excel")
                    print("3. Salir")

                    opcion = input("Ingrese su opción: ")

                    if opcion == '1':
                        df_pacientesclave.to_csv('pacientesporclave.csv', index=False)
                        break
                    elif opcion == '2':
                        df_pacientesclave.to_excel('pacientesporclave.xlsx', index=False)
                        break
                    elif opcion == '3':
                        print("Saliendo del programa...")
                        break
                    else:
                        print("Opción no válida")
                    if not df_pacientesclave:
                        print("No se encontraron datos para la clave del paciente proporcionada.")
                        break
                break
        if opcion == '3':
            while True:
                while True:
                    nombre = input("Ingrese su nombre: ")
                    if not nombre:
                        print("Por favor, no omita el nombre.")
                        continue
                    break

                while True:
                    primer_apellido = input("Ingrese su primer apellido: ")
                    if not primer_apellido:
                        print("Por favor, no omita el primer apellido.")
                        continue
                    break

                segundo_apellido = input("Ingrese su segundo apellido (deje vacío si no cuenta con uno): ")
                from CONSULTASREPORTES import buscar_paciente_nombreapellidos
                df_pacientespornombre = buscar_paciente_nombreapellidos(nombre, primer_apellido, segundo_apellido)
                while True:
                    from ESTADISTICA import dataframe_csv, dataframe_excel
                    print("1. Guardar en CSV")
                    print("2. Guardar en Excel")
                    print("3. Salir")

                    opcion = input("Ingrese su opción: ")

                    if opcion == '1':
                        df_pacientespornombre.to_csv('pacientespornombrecompleto.csv', index=False)
                        break
                    elif opcion == '2':
                        df_pacientespornombre.to_excel('pacientespornombrecompleto.xlsx', index=False)
                        break
                    elif opcion == '3':
                        print("Saliendo del programa...")
                        break
                    else:
                        print("Opción no válida")
                    break  
        if opcion == '4':
           break

def consultas_reportes_menu():
   opciones_consultas_reportes = ['1', '2', '3', '4']
   while True:
        print('Submenu de CONSULTAS Y REPORTES eliga la opcion que desea\n[1]Reportes de citas\n[2]Reportes de pacientes\n[3]Estadisticos demograficos\n[4]Regresar al menu principal')
        opcion = input('R: ')
        if opcion == '':
            print('NO SE DEBE OMITIR EL DATO')
            continue
        if opcion not in opciones_consultas_reportes:
            print('OPCION INVALIDA SOLO SE PUEDEN SELECCIONAR DEL 1 AL 4')
            continue

        if opcion == '1':
            reporte_citas_menu()
        if opcion == '2':
            reportes_pacientes_menu()
        if opcion == '3':
            menu_estadisticos()
        if opcion == '4':
           break

def menu_estadisticos():
    opciones_estadisticos = ['1', '2', '3', '4']
    while True:
        print('Submenu de ESTADISTICOS DEMOGRAFICOS eliga la opcion que desea\n[1]Por edad\n[2]Por sexo\n[3]Por edad y por sexo\n[4]Regresar al menu de consultas y reportes')
        opcion = input('R: ')
        if opcion == '':
            print('NO SE DEBE OMITIR EL DATO')
            continue
        if opcion not in opciones_estadisticos:
            print('OPCION INVALIDA SOLO SE PUEDEN SELECCIONAR DEL 1 AL 4')
            continue

        if opcion == '1':
            while True:
                try:
                    inicio = int(input("Ingrese el inicio del rango de edad: "))
                    fin = int(input("Ingrese el fin del rango de edad: "))
                    if inicio > fin:
                        print("El inicio del rango de edad no puede ser mayor que el final.")
                    else:
                        break
                except ValueError:
                    print("Por favor, ingrese números enteros.")
            
            from ESTADISTICA import estadisticos_edad
            resultado, df_resultado = estadisticos_edad(inicio, fin)
            if resultado is not None:
                print(f"Estadísticas para el rango de edad {inicio} - {fin}:")
                for atributo, valores in resultado.items():
                    print(f"{atributo}:")
                    for estadistica, valor in valores.items():
                        print(f"\t{estadistica}: {valor}")

                while True:
                    from ESTADISTICA import dataframe_csv, dataframe_excel
                    print("1. Guardar en CSV")
                    print("2. Guardar en Excel")
                    print("3. Salir")

                    opcion = input("Ingrese su opción: ")

                    if opcion == '1':
                        df_resultado.to_csv('estadisticosporedad.csv', index=False)
                        break
                    elif opcion == '2':
                        df_resultado.to_excel('estadisticosporedad.xlsx', index=False)
                        break
                    elif opcion == '3':
                        print("Saliendo del programa...")
                        break
                    else:
                        print("Opción no válida")

            else:
                print("No se pudo calcular las estadísticas.")
        elif opcion == '2':
            while True:
                genero = input('Ingrese el sexo (H para Hombre, M para Mujer, N para No contesto): ')
                if genero == "":
                    print("NO SE DEBE OMITIR EL DATO")
                    continue
                if genero.upper() not in ['H', 'M', 'N']:
                    print('OPCIÓN INVÁLIDA. Marque H (HOMBRE), M (MUJER), N (NO CONTESTO). VUELVALO A INTENTAR')
                    continue
                genero = genero.upper()
                break
            from ESTADISTICA import estadisticos_genero
            resultado, df_resultado = estadisticos_genero(genero)
            if resultado is not None:
                print(f"Estadísticas para el género {genero}:")
                for atributo, valores in resultado.items():
                    print(f"{atributo}:")
                    for estadistica, valor in valores.items():
                        print(f"\t{estadistica}: {valor}")


                while True:
                    from ESTADISTICA import dataframe_csv, dataframe_excel
                    print("1. Guardar en CSV")
                    print("2. Guardar en Excel")
                    print("3. Salir")

                    opcion = input("Ingrese su opción: ")

                    if opcion == '1':
                        df_resultado.to_csv('estadisticosporgenero.csv', index=False)
                        break

                    elif opcion == '2':
                        df_resultado.to_excel('estadisticosporgenero.xlsx', index=False)
                        break
                    elif opcion == '3':
                        print("Saliendo del programa...")
                        break
                    else:
                        print("Opción no válida")
            else:
                print("No se pudo calcular las estadísticas.")
        elif opcion == '3':
            while True:
                genero = input('Ingrese el sexo (H para Hombre, M para Mujer, N para No contesto): ')
                if genero == "":
                    print("NO SE DEBE OMITIR EL DATO")
                    continue
                if genero.upper() not in ['H', 'M', 'N']:
                    print('OPCIÓN INVÁLIDA. Marque H (HOMBRE), M (MUJER), N (NO CONTESTO). VUELVALO A INTENTAR')
                    continue
                genero = genero.upper()
                break

            while True:
                try:
                    inicio = int(input("Ingrese el inicio del rango de edad: "))
                    fin = int(input("Ingrese el fin del rango de edad: "))
                    if inicio > fin:
                        print("El inicio del rango de edad no puede ser mayor que el final.")
                    else:
                        rango_edad = (inicio, fin)
                        break
                except ValueError:
                    print("Por favor, ingrese números enteros.")
            
            from ESTADISTICA import estadisticos_genero_edad
            resultado = estadisticos_genero_edad(genero, rango_edad)
            if resultado is not None:
                print(f"Estadísticas para el género {genero} en el rango de edad {rango_edad}:")
                for atributo, valores in resultado.items():
                    print(f"{atributo}:")
                    for estadistica, valor in valores.items():
                        print(f"\t{estadistica}: {valor}")
                while True:
                    from ESTADISTICA import dataframe_csv, dataframe_excel
                    print("1. Guardar en CSV")
                    print("2. Guardar en Excel")
                    print("3. Salir")

                    opcion = input("Ingrese su opción: ")

                    if opcion == '1':
                        df_resultado.to_csv('estadisticosporgeneroedad.csv', index=False)
                        break

                    elif opcion == '2':
                        df_resultado.to_excel('estadisticosporgeneroedad.xlsx', index=False)
                        break
                    elif opcion == '3':
                        print("Saliendo del programa...")
                        break
                    else:
                        print("Opción no válida")
            else:
                print("No se pudo calcular las estadísticas.")

        elif opcion == '4':
            break

def cancelar_citas_menu():
    opciones_cancelar_citas_menu = ['1', '2', '3']
    while True:
        print('Submenu de CANCELACION DE CITAS eliga la opcion que desea\n[1]Busqueda por fecha\n[2]Busqueda por paciente\n[3]Regresar al menu de citas')
        opcion = input('R: ')
        if opcion == '':
            print('NO SE DEBE OMITIR EL DATO')
            continue
        if opcion not in opciones_cancelar_citas_menu:
            print('OPCION INVALIDA SOLO SE PUEDEN SELECCIONAR DEL 1 AL 3')
            continue
        if opcion == '1':
            while True:
                fechausuario = input('Ingresa la fecha de la cita a cancelar FORMATO YYYY-MM-DD: ')
                if fechausuario.strip() == "":
                    print('No se debe omitir el dato')
                    continue
                
                try:
                    fecha_cita = datetime.strptime(fechausuario, '%Y-%m-%d')
                except ValueError:
                    print('Formato de fecha incorrecto. Por favor, ingresa la fecha en el formato correcto (YYYY-MM-DD)')
                    continue
    
                from CONSULTAS import consultar_fechacita_asistenciacita
                consulta = consultar_fechacita_asistenciacita(fecha_cita)
                if consulta:
                    opciones_subconsulta = ['1', '2']
                    for fila in consulta:
                        print(f"Nombre: {fila[0]}, Turno: {fila[1]}\n")
                    opcion = input('DESEAS ELIMINAR LA CITA [1]SI\n[2]NO\n')
                    if opcion == '':
                        print('NO SE DEBE OMITIR EL DATO')
                        continue
                    if opcion not in opciones_subconsulta:
                        print('OPCION INVALIDA SOLO SE PUEDEN SELECCIONAR DEL 1 AL 2')
                        continue
                    if opcion == '1':
                        from DELETE import eliminar_cita_fecha
                        eliminar_cita_fecha(fechausuario)
                        break
                    if opcion == '2':
                        break
                else:
                    print(f"No hay citas registradas para el {fechausuario}.")
                    break
                    
                
        if opcion == '2':
            while True:
                try:
                    from CONSULTAS import consulta_pacientespendientes_citas, obtener_citas_futuras_por_paciente
                    from DELETE import eliminar_cita_folio
                    
                    pacientes_con_citas_pendientes = consulta_pacientespendientes_citas()
                    
                    if not pacientes_con_citas_pendientes:
                        print("No hay pacientes con citas pendientes por realizar.")
                        break
                    else:
                        print("Pacientes con citas pendientes por realizar:")
                        for paciente in pacientes_con_citas_pendientes:
                            nombre_completo = f"{paciente[1]} {paciente[2]} {paciente[3]}"
                            print(f"Folio: {paciente[0]} - Nombre completo: {nombre_completo}")
                        
                        folio_paciente = input("Ingrese el folio del paciente a eliminar: ")
                        citas_paciente = obtener_citas_futuras_por_paciente(folio_paciente)
                        
                        if not citas_paciente:
                            print("El paciente seleccionado no tiene citas pendientes.")
                            break
                        else:
                            print("Citas pendientes del paciente:")
                            for cita in citas_paciente:
                                print(f"Folio: {cita[0]}, Fecha: {cita[1]}, Turno: {cita[2]}")
                            
                            opciones_subconsulta = ['1', '2']
                            opcion = input('DESEAS ELIMINAR LA CITA [1]SI\n[2]NO\n')
                            
                            if opcion == '':
                                print('NO SE DEBE OMITIR EL DATO')
                                continue
                            if opcion not in opciones_subconsulta:
                                print('OPCION INVALIDA SOLO SE PUEDEN SELECCIONAR DEL 1 AL 2')
                                continue
                            
                            if opcion == '1':
                                eliminar_cita_folio(folio_paciente)
                                break
                            if opcion == '2':
                                break
                                
                except Exception as ex:
                    print(f"Se ha producido un error inesperado: {ex}")
                    break                     
                        
        if opcion == '3':
            break

def menu_citas_principal():
   opciones_menu_citas_principal = ['1', '2', '3','4']
   while True:
        print('Submenu de CITAS eliga la opcion que desea\n[1]Programacion de citas\n[2]Realizacion de citas programadas\n[3]Cancelacion de citas\n[4]Regresar al menu principal')
        opcion = input('R: ')
        if opcion == "":
            print('No se debe omitir el dato')
            continue
        if opcion not in opciones_menu_citas_principal:
            print('Opcion invalida seleccione solo las disponibles')
            continue
        if opcion == '1':
            while True:
                from CONSULTAS import consultar_clavepaciente_paciente, consultar_clavepaciente_paciente_maquina
                clavepaciente = input('Ingrese la clave del paciente: ')
                if clavepaciente.strip() == "":
                    print('NO SE DEBE OMITIR EL DATO')
                    continue
                clavepaciente = int(clavepaciente)
                consulta_resultado = consultar_clavepaciente_paciente(clavepaciente)
                if consulta_resultado is None:
                    consultar_clavepaciente_paciente_maquina()
                else:
                    print("Registros del paciente agregados")
                    break

            while True:
                fechacita = input('Ingrese la fecha de la cita (DD/MM/YYYY): ')
                if not fechacita.strip():
                    print('NO SE OMITE EL DATO')
                    continue
                if not validador_fechas(fechacita):
                    print('FORMATO DE FECHA INCORRECTO')
                    continue
                fechacita = datetime.strptime(fechacita, '%d/%m/%Y').date()
                fecha_actual = datetime.now().date()
                if not (fecha_actual <= fechacita):
                    print("\nLa fecha debe ser mayor o igual a la actual. Intente de nuevo.")
                    continue

                if not (fechacita <= fecha_actual + timedelta(days=60)):
                    print("\nLa fecha no puede ser mayor a 60 días después de hoy. Intente de nuevo.")
                    continue

                if fechacita.weekday() == 6:
                    fechacita -= timedelta(days=1)
                    print("La fecha seleccionada cae en domingo. Se propone agendar la cita para el sábado anterior:", fechacita.strftime('%d-%m-%Y'))
                    fecha_confirmada = input("¿Desea confirmar la cita? (SI/NO): ").upper()
                    if fecha_confirmada == "SI":
                        print("La cita ha sido programada para el día", fechacita.strftime('%d/%m/%Y'))
                        break
                    elif fecha_confirmada == "NO":
                        print('ERROR: FECHA INVALIDA')
                        continue
                    else:
                        print('Por favor, responda con "SI" o "NO".')
                        continue
                else:
                    print("La cita ha sido programada para el día", fechacita.strftime('%d/%m/%Y'))
                    break

            while True:
                print("Por favor, ingrese el número correspondiente al turno de la cita:")
                print("  1 mañana\n  2 mediodia\n  3 tarde")
                
                opcion = input('Ingrese el número del turno de la cita: ')
                
                if opcion == "":
                    print('No se debe omitir el dato')
                    continue
                
                if opcion not in tipocita:
                    print('Opción no válida. Por favor, ingrese un número válido.')
                    continue
                
                turnocita = tipocita[opcion]
                print(f'Ha seleccionado el turno de cita: {turnocita}')
                break


            registrar_citas(clavepaciente, fechacita, turnocita)
        if opcion == '2':
            hora, minuto = datetime.now().hour, datetime.now().minute
            horallegada = f'{hora}:{minuto}'

            while True:
              foliocita = input('Ingrese el folio deseado: ')
              if foliocita == "":
                  print('EL DATO NO DEBE OMITIRSE')
                  continue
              break

            while True:
                from CONSULTAS import consultar_clavepaciente_cita, consultar_clavepaciente_cita_maquina
                clavepaciente = input('Ingrese la clave del paciente: ')
                if clavepaciente.strip() == "":
                    print('NO SE DEBE OMITIR EL DATO')
                    continue
                clavepaciente = int(clavepaciente)

                consulta_resultado = consultar_clavepaciente_cita(clavepaciente)

                if consulta_resultado is None:
                    consultar_clavepaciente_cita_maquina()
                else:
                    print("Registros del paciente agregados")
                    break

            while True:
                peso = input('Ingrese el peso: ')
                if peso == "":
                    print('EL DATO NO DEBE OMITIRSE')
                peso = float(peso)
                if peso < 0:
                    print("INGRESE UN PESO CORRECTO, FORMATO INVALIDO")
                    continue
                break

            while True:
                estatura = input('Ingrese la estatura: ')
                if estatura == "":
                    print('ESTE DATO NO DEBE OMITIRSE')
                if not re.match(r"^[0-9]+\.[0-9]{1,2}$", estatura):
                    print('EL FORMATO DEBE LLEVAR UN ENTERO Y 2 DECIMALES')
                    continue
                estatura = float(estatura)
                if estatura < 0:
                    print("INGRESE UNA ESTATURA VALIDA")
                break

            while True:
                presionsistolica = input('Ingrese la presion Sistolica: ')
                if presionsistolica == "":
                    print('ESTE DATO NO DEBE OMITIRSE')
                presionsistolica = float(presionsistolica)
                if presionsistolica < 0:
                    print("DEBE SER NUMERO ENTERO A TRES DIGITOS(999), FORMATO INVALIDO")
                    continue
                break

            while True:
                presiondiastolica = input('Ingrese la presion Diastolica: ')
                if presiondiastolica == "":
                    print('ESTE DATO NO DEBE OMITIRSE')
                presiondiastolica = float(presiondiastolica)
                if presiondiastolica < 0:
                    print("DEBE SER NUMERO ENTERO A TRES DIGITOS(999), FORMATO INVALIDO")
                    continue
                break

            while True:
                diagnostico = input('Ingrese el diagnostico: ')
                if diagnostico == "":
                    print('ESTE DATO NO DEBE OMITIRSE')
                if len(diagnostico) > 200:
                    print('LONGITUD MAXIMA DE 200 CARACTERES, INTENTE DE NUEVO')
                    continue
                break
            citas_realizadas(foliocita, clavepaciente, horallegada, peso, estatura, presionsistolica, presiondiastolica, diagnostico)

        if opcion == '3':
            cancelar_citas_menu()
        if opcion == '4':
            break

def menu_principal():
    while True:
        opcionesmenuprincipal = ['1', '2', '3', '4']
        print('\nximenadoctora XXXX elige la opción que deseas:\n[1] Registro de pacientes\n[2] Citas\n[3] Consultas y reportes\n[4] Salir del sistema')
        opcion = input('R: ')
        if opcion == '':
            print('NO SE DEBE OMITIR EL DATO')
            continue
        if opcion not in opcionesmenuprincipal:
            print('OPCIÓN INVÁLIDA. SOLO SE PUEDEN SELECCIONAR DEL 1 AL 4')
            continue
        if opcion == '1':
            while True:
                primerapellido = input('Ingrese el Primer Apellido: ')
                if primerapellido == "":
                    print('NO SE DEBE OMITIR EL DATO')
                    continue
                break

            segundoapellido = input('Ingrese el Segundo Apellido: ')

            while True:
                nombre = input('Ingrese el Nombre: ')
                if nombre == "":
                    print('NO SE DEBE OMITR EL DATO')
                    continue
                break

            while True:
                fechanacimiento = input('Ingrese la fecha de nacimiento (DD/MM/AAAA): ')
                if not validador_fechas(fechanacimiento):
                    print('FORMATO DE FECHA INCORRECTO. Debe ser: DD/MM/AAAA')
                    continue
                fecha_nacimiento = datetime.strptime(fechanacimiento, '%d/%m/%Y')
                fecha_actual = datetime.now()
                edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
                break

            while True:
                sexo = input('Ingrese el sexo (H para Hombre, M para Mujer, N para No contesto): ')
                if sexo == "":
                    print("NO SE DEBE OMITIR EL DATO")
                    continue
                if sexo.upper() not in ['H', 'M', 'N']:
                    print('OPCIÓN INVÁLIDA. Marque H (HOMBRE), M (MUJER), N (NO CONTESTO). VUELVALO A INTENTAR')
                    continue
                sexo = sexo.upper()
                break


            registrar_pacientes(primerapellido, segundoapellido, nombre, fechanacimiento, sexo, edad)

        if opcion == '2':
            menu_citas_principal()
        if opcion == '3':
            consultas_reportes_menu()
        if opcion == '4':
            break

menu_principal()