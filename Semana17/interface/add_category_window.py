import PySimpleGUI as sg

def add_category_layout(manager, file_name):
    category_layout = [
        [sg.Text("Categorias")],
        [sg.Text("Nombre de la categoria"), sg.Input(key='-TITLE-')],
        [sg.Button("Guardar"), sg. Button("Regresar")]
    ]

    window = sg.Window("Pantalla de Categorias", category_layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Regresar":
            break
        elif event == "Guardar":
            title = values['-TITLE-']

            if not title.strip():
                sg.popup("Debes ingresar el nombre del nuevo movimiento...")
                continue

            if not manager.add_category(title):
                sg.popup("La categoria ya existe")
                continue

            manager.export_data(file_name)
            window['-TITLE-'].update('')
            sg.popup("Categoria registrada")
    
    window.close()