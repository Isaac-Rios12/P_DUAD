import PySimpleGUI as sg
from new_transaction_window import show_movement_layout
from add_category_window import show_category_layout
data = [
    [20, 20500]
]

layout = [
    [sg.Text("Sistema de gestion de finanzas...")],
    [sg.Table(
        values = data,
        headings = ["Gastos", "Ingresos"],
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
        show_movement_layout()
        window.un_hide()
    
    if event == "-INCOME-":
        window.hide()
        show_movement_layout()
        window.un_hide()
    
    elif event == "-CATEGORY-":
        window.hide()
        show_category_layout()
        window.un_hide()

    elif event == sg.WIN_CLOSED:
        break
window.close()

