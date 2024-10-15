from flask import Flask, jsonify, request
from Week1.data import Task

from Week1.logic import check_id, delete

app = Flask(__name__)

task_instance = Task()
task_instance.import_data("tareas.json")


@app.route('/Tasks', methods=["GET", "POST"])
def create_task():

    if request.method == "GET":
        data = task_instance.get_task()
        return jsonify(data)
    else:
        try:
            if "id" not in request.json:
                raise ValueError("Debes ingresar el id")

            id = request.json['id']
            exists, tarea= check_id(id, task_instance)

            if not exists:

                new_data = {
                    "id": request.json["id"],
                    "titulo": request.json["titulo"],
                    "descripcion": request.json["descripcion"],
                    "estado": request.json["estado"]
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
    print(f"Intentando eliminar la tarea con ID: {id}")  # Agregar log para depuración
    exists, tarea = check_id(id, task_instance)
    
    print(f"Existencia de la tarea: {exists}, Tarea: {tarea}")  # Verificar el resultado

    if exists:
        delete(tarea, task_instance)
        task_instance.export_data("tareas.json")  # Asegúrate de guardar los cambios
        return jsonify(message="Tarea eliminada con éxito"), 200
    else:
        return jsonify(message="Tarea no encontrada"), 404  # Cambié 400 a 404 para semántica






if __name__ == "__main__":
    app.run(host="localhost", debug=True)