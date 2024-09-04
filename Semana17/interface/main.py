import PySimpleGUI as sg
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
        [sg.Button("Nuevo Movimiento")],
        [sg.Button("Nueva Categoria  ")]
    ], vertical_alignment='top')
    ]
]

window = sg.Window("Gestion de finanzas...", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
window.close()

