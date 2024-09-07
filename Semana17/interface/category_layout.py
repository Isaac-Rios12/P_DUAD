import PySimpleGUI as sg

def show_category_layout():
    category_layout = [
        [sg.Text("Categorias")],
        [sg.Text("Nombre de la categoria"), sg.Input()],
        [sg.Button("Guardar"), sg. Button("Regresar")]
    ]

    window = sg.Window("Pantalla de Categorias", category_layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Regresar":
            break
        elif event == "Guardar":
            sg.popup("Categoria registrada")
    
    window.close()