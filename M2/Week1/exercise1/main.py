from flask import Flask, jsonify, request
from exercise1.data import TaskManager
from exercise1.logic import is_valid_status

app = Flask(__name__)

task_instance = TaskManager()
task_instance.import_data("tareas.json")


@app.route('/Tasks', methods=["GET", "POST"])
def create_task():

    if request.method == "GET":
        data = task_instance.get_tasks()
        return jsonify(data)
    else:
        try:
 
            if "id" not in request.json:
                raise ValueError("Debes ingresar el id")
            if "titulo" not in request.json:
                raise ValueError("Debes ingresar el titulo")
            if "descripcion" not in request.json:
                raise ValueError("Debes ingresar la descripcion")
            if "estado" not in request.json:
                raise ValueError("Debes ingresar el etsado")

            state = request.json.get("estado")
            state_error = is_valid_status(state)
            if state_error:
                return jsonify(state_error), 400
            

            id = request.json['id']
            exists, tarea = task_instance.check_id(id)

            if not exists:

                new_data = {
                    "id": request.json.get("id"),
                    "titulo": request.json.get("titulo"),
                    "descripcion": request.json.get("descripcion"),
                    "estado": state
                }

                task_instance.add_task(new_data)
                task_instance.export_data("tareas.json")
                return jsonify(message="Tarea agregada con éxito"), 201
                

            else:
                return jsonify(message="Id ya registrado...."), 400

        except ValueError as ex:
            return jsonify(message=str(ex)), 400
        except Exception as ex:  
            return jsonify(message=str(ex)), 500

@app.route('/Tasks/<string:id>', methods=["DELETE"])
def delete_task(id):

    if not id or id.strip()=="":
        return jsonify(message="ID no proporcionado o invalido"), 400
    
    exists, tarea = task_instance.check_id(id)

    if exists:
        task_instance.remove_task(tarea)
        task_instance.export_data("tareas.json")  
        return jsonify(message="Tarea eliminada con éxito"), 200
    else:
        return jsonify(message="Tarea no encontrada"), 404  


@app.route('/Tasks/<string:id>', methods=["PATCH"])
def update_task(id):

    exists, tarea = task_instance.check_id(id)

    new_status = request.json.get("estado")

    if new_status is None or new_status.strip() == "":
        return jsonify(message="El campo estado es requerido"), 400

    if not exists:
        return jsonify(message="Tarea no encontrada"), 400

    state_error = is_valid_status(new_status)
    if state_error:
        return jsonify(state_error), 400

    if tarea["estado"] == new_status:
        return jsonify(message="No se realizan cambios, estado es el mismo"), 200
    
    response = task_instance.update_task_logic(tarea, new_status)
    return response


if __name__ == "__main__":
    app.run(host="localhost", debug=True)