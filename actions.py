


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
        if keep_asking == 1 or keep_asking == 2:
            return keep_asking == 1
        else:
            print("opcion fuera de rango")
    except ValueError:
        print("valor no valido")


def add_student(students_list):
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


def show_students(students_list):
    try:
        for student in students_list:
            print("ESTUDIANTE:       ", student["Name"])
            print("Seccion:          ", student["Section"])
            print("Nota de espanol:  ", student["Spanish grade"])
            print("Nota de ingles:   ", student["English grade"])
            print("Nota de sociales: ", student["Social grade"])
            print("Nota de ciencias: ", student["Science grade"])
            print("Promedio:         ", student["Average"])
            print("-------------------------------------------------")
            
    except Exception:
        print("Error al mostrat la lista...")


def show_top_3_best_average_grade(students_list):
    try:
        sort_students_list = sorted(students_list, key=lambda x: float(x["Average"]), reverse=True)
        print("Los mejores 3 estudiantes son:")
        for i in range(min(3, len(sort_students_list))):
            student = sort_students_list[i]
            print(f"Nombre:   {student['Name']}")
            print(f"Sección:  {student['Section']}")
            print(f"Promedio: {student['Average']}")
            print("--------------------")
            
    except KeyError:
        print("Error al ordenar la lista...")


def average_of_all_students(students_list):
    try:
        total_average= 0
        for student in students_list:
            total_average += float(student["Average"])
            
        total_average /= len(students_list)
        print(f"El promedio total es de...{total_average}")
        
    except KeyError:
        print("Error...")


