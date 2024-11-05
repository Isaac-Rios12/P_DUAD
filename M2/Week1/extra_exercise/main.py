from flask.views import MethodView
from flask import Flask, jsonify, request
from extra_exercise.logic import is_valid_status
from extra_exercise.data import TaskManager

app = Flask(__name__)

class TaskAPI(MethodView):

    def __init__(self):
        self.task_instance = TaskManager()
        self.task_instance.import_data("tareas.json")

    def get(self):
        data = self.task_instance.get_tasks()
        return jsonify(data)

    def post(self):
        try:
            if "id" not in request.json:
                raise ValueError("Debes ingresar el id")
            if "titulo" not in request.json:
                raise ValueError("Debes ingresar el titulo")
            if "descripcion" not in request.json:
                raise ValueError("Debes ingresar la descripcion")
            if "estado" not in request.json:
                raise ValueError("Debes ingresar el estado")

            state = request.json.get("estado")
            state_error = is_valid_status(state)

            if state_error:
                return jsonify(state_error), 400

            id = request.json['id']
            exists, tarea = self.task_instance.check_id(id)

            if not exists:
                new_data = {
                    "id": request.json.get("id"),
                    "titulo": request.json.get("titulo"),
                    "descripcion": request.json.get("descripcion"),
                    "estado": request.json.get("estado")
                }

                self.task_instance.add_task(new_data)
                self.task_instance.export_data("tareas.json")
                return jsonify(message="Tarea agregada con éxito"), 201
            
            else:
                return jsonify(message="Id de tarea ya existe"), 400

        except ValueError as ex:
            return jsonify(message=str(ex)), 400
        except Exception as ex:
            return jsonify(message=str(ex)), 500

    def delete(self, id):
        if not id or id.strip() == "":
            return jsonify(message="Id no proporcionado o inválido"), 400
        
        exists, tarea = self.task_instance.check_id(id)

        if exists:
            self.task_instance.remove_task(tarea)
            self.task_instance.export_data("tareas.json")
            return jsonify(message="Tarea eliminada con éxito"), 200
        else:
            return jsonify(message="Tarea no encontrada"), 404

    def patch(self, id):
        exists, tarea = self.task_instance.check_id(id)

        new_status = request.json.get("estado")

        if new_status is None or new_status.strip() == "":
            return jsonify(message="El campo estado es requerido"), 400

        if not exists:
            return jsonify(message="Tarea no encontrada"), 404

        state_error = is_valid_status(new_status)

        if state_error:
            return jsonify(state_error), 400
        
        if tarea['estado'] == new_status:
            return jsonify(message="No se realizan cambios, el estado es el mismo"), 200

        response = self.task_instance.update_task_logic(tarea, new_status)
        return response

def register_api(app, name):
    task_view = TaskAPI.as_view(f"{name}-item")
    app.add_url_rule(f"/{name}", view_func=task_view, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/<string:id>", view_func=task_view, methods=["DELETE", "PATCH"])

register_api(app, "Tasks")

if __name__ == "__main__":
    app.run(host="localhost", debug=True)
