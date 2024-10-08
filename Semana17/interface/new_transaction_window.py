import PySimpleGUI as sg
from .add_category_window import add_category_layout

#aprendi que si instancio aca no refleja lo que ya esa clase a cargado anteriormente...

def show_movement_window(manager, t_type, file_name):

    
    categories = manager.get_categories()
    

    movement_layout = [
        [sg.Text("Movimientos....")],
        [sg.Text("Titulo del movimiento"), sg.Input(key='-TITLE-')],
        [sg.Text("Seleccione la categoria"), sg.Combo(categories, key='-CATEGORY-'), sg.Button("Nueva Categoria  ", key='-NEWCATEGORY-')],
        [sg.Text("Ingrese el monto"), sg.Input(key='-AMOUNT-')],
        [sg.Button("Guardar"), sg.Button("Regresar")]
    ]

    window = sg.Window("Pantalla de movimientos", movement_layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Regresar":
            break

        elif event == "-NEWCATEGORY-":
            window.hide()
            add_category_layout(manager, file_name)
            window.un_hide()

            categories = manager.get_categories()
            window['-CATEGORY-'].Update(values=categories)

            

        elif event == "Guardar":
            title = values['-TITLE-']
            amount = values['-AMOUNT-']
            category_selected = values['-CATEGORY-']
            transaction_type = t_type

            
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

            manager.add_transaction(title, amount, category_selected, transaction_type)
            manager.export_data(file_name)
            sg.popup("Movimiento Guardado...")

            window['-TITLE-'].Update('')
            window['-AMOUNT-'].Update('')
            window['-CATEGORY-'].Update('')
            

    window.close()