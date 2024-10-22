from flask.views import MethodView
from flask import Flask, jsonify, request
from extra_exercise.logic import check_id, is_valid_status, remove_task
from extra_exercise.data import Task


app = Flask(__name__)


class TaskAPI(MethodView):

    def __init__(self):
        self.task_instance = Task()
        self.task_instance.import_data("tareas.json")

    def get(self):
        data = self.task_instance.get_task()
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
            exists, tarea = check_id(id, self.task_instance)

            if not exists:
                new_data = {
                    "id": request.json.get("id"),
                    "titulo": request.json.get("titulo"),
                    "descripcion": request.json.get("descripcion"),
                    "estado": request.json.get("estado")
                }

                self.task_instance.add_task(new_data)
                self.task_instance.export_data("tareas.json")
                return jsonify(message="Tarea agregada con eexito"), 200
            
            else:
                return jsonify(message="Id de tarea ya existe"), 400
            
        except ValueError as ex:
            return jsonify(message=str(ex)), 400
        except ValueError as ex:
            return jsonify(message=str(ex)), 500


    def delete_task(self, id):
        if not id or id.strip()=="":
            return jsonify(message="Id no proporcionado o invalido"), 400
        
        exists, tarea = check_id(id, self.task_instance)

        if exists:
            remove_task(tarea, self.task_instance)
            self.task_instance.export_data("tareas.json")
            return jsonify(message="tarea eliminadaa....."), 200
        else:
            return jsonify(message="Tarea no enconntrada"), 404

    def update_task(self, id):

        exists, tarea = check_id(id, self.task_instance)

        new_status = request.json.get("estado")

        if new_status is None or new_status.strip() == "":
            return jsonify(message="El campo estado es requerido"), 400

        if not exists:
            return jsonify(message="La tarea no existe"), 400

        state_error = is_valid_status(new_status)

        if state_error:
            return jsonify(state_error), 400
        
        if tarea['estado'] == new_status:
            return jsonify(message="No se realizan cambios, el estado es el mismo"), 200

        response = self.task_instance.update_task_logic(tarea, new_status)
        return response



task_api = TaskAPI()
app.add_url_rule('/Tasks', view_func=task_api.get, methods=["GET"])
app.add_url_rule('/Tasks', view_func=task_api.post, methods=["POST"])
app.add_url_rule('/Tasks/<string:id>', view_func=task_api.delete_task, methods=["DELETE"])
app.add_url_rule('/Tasks/<string:id>', view_func=task_api.update_task, methods=["PATCH"])

if __name__ == "__main__":
    app.run(host="localhost", debug=True)




