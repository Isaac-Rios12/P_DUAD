from Week1.data import Task

def check_id(id, task_instance):
    for tarea in task_instance.get_task():
        if tarea["id"] == id:
            return True, tarea
    return False, None

def remove_task(tarea, task_instance):
    task_instance.get_task().remove(tarea)


def is_valid_status(state):
    allowed_states = {"POR HACER", "EN PROCESO", "ACEPTADA"}

    if state.upper() not in allowed_states:
        return({"error": "Estado invalido, Los estados validos son : POR HACER, EN PROCESO, ACEPTADA "})
    return None


    