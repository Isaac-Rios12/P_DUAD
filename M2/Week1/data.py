import json
import os

class Task():
    def __init__(self):
        self.tareas_list = []

    def import_data(self, file):
        try:
            if not os.path.exists(file):
                print("El doc no existe...")
            
            with open(file, 'r', encoding='utf-8') as f:
                
                saved_data = json.load(f)
                self.tareas_list = saved_data

        except json.JSONDecodeError:
            print("Error al leer el archivo")
        except Exception as e:
            print(f("Ocurrio un error: {e}"))

    def export_data(self, file):
        try: 
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(self.tareas_list, f, indent=4)
                print("Agregado...")
        except Exception as e:
            print(f("Ocurrio un error: {e}"))

    def get_task(self):
        return self.tareas_list
    
    def add_task(self, new_task):
        self.tareas_list.append(new_task)

