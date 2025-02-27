import json
import os


class TaskManager():
    def __init__(self):
        self.tasks_list = []

    def get_tasks(self):
        return self.tasks_list

    def import_data(self, file):
        try:
            if not os.path.exists(file):
                print("El doc no existe...")
            
            with open(file, 'r', encoding='utf-8') as f:
                
                saved_data = json.load(f)
                self.tasks_list = saved_data

        except json.JSONDecodeError:
            print("Error al leer el archivo")
        except Exception as e:
            print(f("Ocurrio un error: {e}"))

    def export_data(self, file):
        try: 
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks_list, f, indent=4)
                print("Agregado...")
        except Exception as e:
            print(f("Ocurrio un error: {e}"))
    
    def add_task(self, new_task):
        self.tasks_list.append(new_task)

    def update_task_logic(self, tarea, new_status):

        #exists, tarea = check_id(id, task_instance)

        tarea["estado"] = new_status
        self.export_data("tareas.json")
        return {"message": "Estado actualizado correctamente...", "tarea": tarea}, 200

    def check_id(self, id):
        for tarea in self.tasks_list:
            if tarea["id"] == id:
                return True, tarea
        return False, None

    def remove_task(self, tarea):
        self.tasks_list.remove(tarea)


 




