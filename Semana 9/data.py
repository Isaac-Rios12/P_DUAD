import csv

class Student():
    def __init__(self, name, section, spanish_grade, english_grade, social_grade, science_grade):
        self.name = name
        self.section = section
        self.spanish_grade = spanish_grade
        self.english_grade = english_grade
        self.social_grade = social_grade
        self.science_grade = science_grade
        self.average = self.calculate_average()

    def get_name(self):
        return self.name 
        
    def get_section(self):
        return self.section
        
    def get_spanish_grade(self):
        return self.spanish_grade

    def get_english_grade(self):
        return self.english_grade

    def get_social_grade(self):
        return self.social_grade

    def get_science_grade(self):
        return self.science_grade

    def calculate_average(self):
        return (self.spanish_grade + self.english_grade + self.social_grade + self.science_grade) / 4



def export_csv_file(file_path, data, headers):
    try:
        with open(file_path, 'w',  newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for student in data:
                writer.writerow({
                    'Name': student.name,
                    'Section': student.section,
                    'Spanish grade': student.spanish_grade,
                    'English grade': student.english_grade,
                    'Social grade': student.social_grade,
                    'Science grade': student.science_grade,
                    'Average': student.average
                })
            print("exportado con exito")
            
    except Exception:
        print(f"Error al exportar los datos")


def import_csv_file(students_list, file_path): 
    try: 
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                 student = Student(row['Name'], row['Section'], float(row['Spanish grade']), float(row['English grade']), float(row['Social grade']), float(row['Science grade']))
                 students_list.append(student)
            print("Documento importado...")

    except FileNotFoundError:
        print("Archivo no encontrado...")
        return []

    except csv.Error:
        print("Error al procesar el archivo...")
        return []
    except Exception as ex:
        print(f"error: {ex}")
        return []
