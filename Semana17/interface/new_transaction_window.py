import PySimpleGUI as sg

def show_movement_layout():
    
    categorias = ["alimentos", "Transporte"]

    movement_layout = [
        [sg.Text("Movimientos....")],
        [sg.Text("Titulo del movimiento"), sg.Input(key='-TITLE-')],
        [sg.Text("Seleccione la categoria"), sg.Combo(categorias, key='-CATEGORY-')],
        [sg.Text("Ingrese el monto"), sg.Input(key='-AMOUNT-')],
        [sg.Button("Guardar"), sg.Button("Regresar")]
    ]

    window = sg.Window("Pantalla de movimientos", movement_layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Regresar":
            break
        elif event == "Guardar":
            title = values['-TITLE-']
            category_selected = values['-CATEGORY-']
            amount = values['-AMOUNT-']

            if not title.strip():
                sg.popup("Debes ingresar un titulo...")
                continue

            if not category_selected:
                sg.popup("Debes seleccionar una categoria")
                continue
            
            try:
                amount = float(amount)
                if amount <= 0:
                    sg.popup("Ingresa un numero mayor a 0")
                    continue
            except ValueError:
                sg.popup("Ingresa un monto valido.")
                continue

            
            sg.popup("Movimiento Guardado...")

    window.close()