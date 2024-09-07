import PySimpleGUI as sg
from transaction_layout import show_movement_layout
from category_layout import show_category_layout
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
        [sg.Button("Nueva Categoria  ")]
    ], vertical_alignment='top')
    ]
]

window = sg.Window("Gestion de finanzas...", layout)

while True:
    event, values = window.read()
    
    if event == "Nuevo Gasto":
        window.hide()
        show_movement_layout("Expense")
        window.un_hide()
    
    if event == "Nuevo Ingreso":
        window.hide()
        show_movement_layout("Income")
        window.un_hide()
    
    elif event == "Nueva Categoria  ":
        window.hide()
        show_category_layout()
        window.un_hide()

    elif event == sg.WIN_CLOSED:
        break
window.close()

