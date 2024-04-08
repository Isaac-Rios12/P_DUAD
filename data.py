import csv



def export_csv_file(file_path, data, headers):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            writer = csv.DictWriter(file, headers)
            writer.writeheader()
            writer.writerows(data)
            print("exportado con exito")
            
    except Exception:
        print(f"Error al exportar los datos")


def import_csv_file(students_list, file_path): 
    try: 
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            imported_list = list(reader)
            print("Documento importado....")
            print(imported_list)
            students_list.extend(imported_list)
            #return imported_list

    except FileNotFoundError:
        print("Archivo no encontrado...")
        return []

    except csv.Error:
        print("Error al procesar el archivo...")
        return []
    except Exception as ex:
        print(f"error: {ex}")
        return []
