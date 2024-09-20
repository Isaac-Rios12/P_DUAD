
import PySimpleGUI as sg

from .new_transaction_window import show_movement_window
from .add_category_window import add_category_layout
from logic.Logic import load_data


def main_window(manager, file_name):

    rows = load_data(manager, file_name)

    headers = ['Titulo', 'Monto', 'Categoria', 'Tipo']
    layout = [
        [sg.Text("Sistema de gestion de finanzas...")],
        [sg.Table(
            values = rows,
            headings = headers,
            key = '-TABLE-',
            #auto_size_columns=False,
            justification = 'center'
        ),
        sg.Column([
            [sg.Button("Nuevo Gasto", key='-EXPENSE-')],
            [sg.Button("Nuevo Ingreso", key='-INCOME-')],
            [sg.Button("Nueva Categoria  ", key='-CATEGORY-')]
        ], vertical_alignment='top')
        ]
    ]

    window = sg.Window("Gestion de finanzas...", layout)

    while True:
        event, values = window.read()
        
        if event == "-EXPENSE-":
            window.hide()
            show_movement_window(manager,"Gasto", file_name)
            window.un_hide()
            #actualizo
            rows = load_data(manager, file_name)
            window['-TABLE-'].update(values=rows)
        
        if event == "-INCOME-":
            window.hide()
            show_movement_window(manager, "Ingreso", file_name)
            window.un_hide()
            #actualizo
            rows = load_data(manager, file_name)
            window['-TABLE-'].update(values=rows)
        
        elif event == "-CATEGORY-":
            window.hide()
            add_category_layout(manager, file_name)
            window.un_hide()

        elif event == sg.WIN_CLOSED:
            break
    window.close()
