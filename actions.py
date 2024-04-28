from data import Student


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
            section = input("Ingrese la seccion del estudiante...")
            spanish_grade = ask_grade("Espanol")
            english_grade = ask_grade("Ingles")
            social_grade = ask_grade("Sociales")
            science_grade = ask_grade("Ciencias")

            
            student = Student(name_student, section, spanish_grade, english_grade, social_grade, science_grade)
            students_list.append(student)
            
            if not ask_if_keep_adding_student():
                break
            
        except ValueError:
            print("error encontrado")


def show_students(students_list):
    try:
        for student in students_list:
            print("ESTUDIANTE:       ", student.get_name())
            print("Seccion:          ", student.get_section())
            print("Nota de espanol:  ", student.get_spanish_grade())
            print("Nota de ingles:   ", student.get_english_grade())
            print("Nota de sociales: ", student.get_social_grade())
            print("Nota de ciencias: ", student.get_science_grade())
            print("Promedio:         ", student.calculate_average())
            print("-------------------------------------------------")
            
    except Exception:
        print("Error al mostrat la lista...")


def show_top_3_best_average_grade(students_list):
    try:
        sort_students_list = sorted(students_list, key=lambda x: x.calculate_average(), reverse=True)
        print("Los mejores 3 estudiantes son:")
        for i in range(min(3, len(sort_students_list))):
            student = sort_students_list[i]
            print(f"Nombre:   {student.get_name()}")
            print(f"Sección:  {student.get_section()}")
            print(f"Promedio: {student.calculate_average()}")
            print("--------------------")
            
    except ValueError as ve:
        print(f"Error al convertir un valor a un número: {ve}")
    except TypeError as te:
        print(f"Error de tipo al ordenar la lista: {te}")
    except Exception as e:
        print(f"Error desconocido: {e}")

def average_of_all_students(students_list):
    try:
        total_average = 0
        for student in students_list:
            total_average += student.calculate_average()
            
        total_average /= len(students_list)
        print(f"El promedio total es de...{total_average}")
        
    except Exception:
        print("Error al calcular el promedio total...")


