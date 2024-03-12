import csv

students_list = []

def ask_grade(subject):
    while True:
        try :
            grade = int(input(f"Ingrese la nota de: {subject} "))
            if grade >= 0 and grade <= 100:
                return grade
            else:
                print("la nota esta fuera de rango...")
            
        except ValueError:
            print("gas ingresado un valor no valido...")
            
def ask_if_keep_adding_student():
    try:
        keep_asking = int(input("Elige una opcion: 1.Ingresar otra estudiante 2.Salir..."))
        if keep_asking == 1:
            return True
        elif keep_asking == 2:
            print("Redirigiendo al mnu principal...")
            return False
        else:
            print("opcion fuera de rango")
    except ValueError:
        print("valor no valido")
        

def add_student():
    while True:
        try:
            name_student = input("Ingrese el nombre completo del estudiante...")
            seccion = input("Ingrese la seccion del estudiante...")
            spanish_grade = ask_grade("Espanol")
            english_grade = ask_grade("Ingles")
            social_grade = ask_grade("Sociales")
            science_grade = ask_grade("Ciencias")
            average_student = (spanish_grade + english_grade + science_grade + social_grade) / 4
            
            student = {
                "Name": name_student,
                "Section": seccion,
                "Spanish grade": spanish_grade,
                "English grade": english_grade,
                "Social grade": social_grade,
                "Science grade": science_grade,
                "Average": average_student
            }
            students_list.append(student)
            
            #ask_if_keep_adding_student()
            
            if not ask_if_keep_adding_student():
                break
            
        except ValueError:
            print("error encontrado")
            
    #print(students_list)
    #return students_list

def show_students():
    for student in students_list:
        print("ESTUDIANTE:       ", student["Name"])
        print("Seccion:          ", student["Section"])
        print("Nota de espanol:  ", student["Spanish grade"])
        print("Nota de ingles:   ", student["English grade"])
        print("Nota de sociales: ", student["Social grade"])
        print("Nota de ciencias: ", student["Science grade"])
        print("Promedio:         ", student["Average"])
        print("-------------------------------------------------")

def show_top_3_best_average_grade():
    #sort_students_list = students_list.sort(key=lambda x: x["Average"])
    #students_list.sort(key=lambda x: x["Average"], reverse=True)
    #print(students_list)
    #print()
    sort_students_list = sorted(students_list, key=lambda x: x["Average"], reverse=True)
    print("Los mejores 3 estudiantes son:")
    for i in range(min(3, len(sort_students_list))):
        student = sort_students_list[i]
        print(f"Nombre: {student['Name']}")
        print(f"Sección: {student['Section']}")
        print(f"Promedio: {student['Average']}")
        print("--------------------")
def menu():
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
                option = int(input ("Ingrese la opcion necesaria"))
                if option == 1:
                    add_student()
                elif option == 2:
                    show_students()
                elif option == 3:
                    show_top_3_best_average_grade()
                elif option == 4:
                    print("has entrado a la opcion 4")
                elif option == 5:
                    print("has entrado a la opcion 5")
                elif option == 6:
                    print("has entrado a la opcion 6")
                elif option == 7:
                    print("has salido del sistema, GRACIAS!!!!")
                    break
                else:
                    print("opcion fuera de rango\n")
        except ValueError:
            print("Valor no valido....")
        

menu()
