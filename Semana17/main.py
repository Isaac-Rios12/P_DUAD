from data.classes import FinanceManager
from interface.main_window import main_window

def main():
    file_name = "Finanzas.json"
    mn = FinanceManager()
    main_window(mn, file_name)

if __name__ == "__main__":
    main()
