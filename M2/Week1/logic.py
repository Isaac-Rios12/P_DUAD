from Week1.data import Task



def check_id(id, task_instance):
    for tarea in task_instance.get_task():
        if tarea["id"] == id:
            return True, tarea
    return False, None

def delete(tarea, task_instance):
    task_instance.get_task().remove(tarea)
    