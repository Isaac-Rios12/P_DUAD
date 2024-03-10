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
            
def add_student():
    while True:
        try:
            name_student = input("Ingrese el nombre completo del estudiante...")
            seccion = input("Ingrese la seccion del estudiante...")
            spanish_grade = ask_grade("Espanol")
            english_grade = ask_grade("Ingles")
            social_grade = ask_grade("Sociales")
            science_grade = ask_grade("Ciencias")
            
            keep_asking = int(input("Elige una opcion: 1.Ingresar otra estudiante 2.Salir..."))
            if keep_asking == 2:
                print("Redirigiendo al mnu principal...")
                break
        except ValueError:
            print("error encontrado")

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
                    print("has entrado a la opcion 2")
                elif option == 3:
                    print("has entrado a la opcion 3")
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
