def menu():
    try:
        while True:
            print('''
1. Ingresar estudiante
2. Opcion 2
3. oPcio 3 
4. Opcion 4
5. Opcion 5
6. salir''')
            option = int(input ("Ingrese la opcion necesaria"))
            if option == 1:
                print("has entrado a la opcion 1")
            elif option == 2:
                print("has entrado a la opcion 2")
            elif option == 3:
                print("has entrado a la opcion 3")
            elif option == 4:
                print("has entrado a la opcion 4")
            elif option == 5:
                print("has entrado a la opcion 5")
            elif option == 6:
                print("has salido del sistema, GRACIAS!!!!")
                break
            else:
                print("opcion fuera de rango\n")
    except ValueError:
        print("Valor no valido....")
        
menu()
