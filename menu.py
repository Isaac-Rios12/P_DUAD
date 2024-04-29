#from actions import add_student, show_students, show_top_3_best_average_grade, average_of_all_students
import actions

from data import export_csv_file, import_csv_file

students_headers = (
    'Name',
    'Section',
    'Spanish grade',
    'English grade',
    'Social grade',
    'Science grade',
    'Average'
)

def menu():
    students_list = []

    while True:
        try:
            print('''
    1. Ingresar estudiante
    2. Ver informacion de estudiantes ingresados.
    3. Top 3 de los estudiantes con mejor promedio
    4. Ver nota promedio de todas las notas
    5. Exportar datos a CSV
    6. Importar datos ya exprotados CSV
    7. salir''')
            option = int(input("Ingrese la opcion necesaria..."))
            if option == 1:
                actions.add_student(students_list)
            elif option == 2:
                actions.show_students(students_list)
            elif option == 3:
                actions.show_top_3_best_average_grade(students_list)
            elif option == 4:
                actions.average_of_all_students(students_list)
            elif option == 5:
                export_csv_file('students_list.csv', students_list, students_headers )
            elif option == 6:
                import_csv_file(students_list, 'students_list.csv')
            elif option == 7:
                print("has salido del sistema, GRACIAS!!!!")
                break
            else:
                print("opcion fuera de rango\n")
        except ValueError:
            print("Valor no valido....")
