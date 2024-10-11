from flask import Flask, jsonify, request
from Week1.data import Task

app = Flask(__name__)


tasks_list = [
    {
        "id": "1",
        "titulo": "Sacar mascotas",
        "descripcion": "no olvidar",
        "estado": "por hacer"
    }
]

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
            if not check_id(id):

                tasks_list.append(
                    {
                    
                    "id": request.json["id"],
                    "titulo": request.json["titulo"],
                    "descripcion": request.json["descripcion"],
                    "estado": request.json["estado"]

                }
                )
                return tasks_list
            else:
                return jsonify(message="Id ya registrado...."), 400

        except ValueError as ex:
            return jsonify(message=str(ex)), 400
        except Exception as ex:  
            return jsonify(message=str(ex)), 500

def check_id(id):
    for tarea in tasks_list:
        if tarea["id"] == id:
            return True
    return False

if __name__ == "__main__":
    app.run(host="localhost", debug=True)