

def is_valid_status(state):
    allowed_states = ["POR HACER", "EN PROCESO", "ACEPTADA"]

    if state.upper() not in allowed_states:
        return({"error": "Estado invalido, Los estados validos son : POR HACER, EN PROCESO, ACEPTADA "})
    return None





    