
def load_data(fm, file):

    try:

        data = fm.import_data(file)

        rows = []

        for item in data['transactions']:
            row = [
                item['title'],
                item['amount'],
                item['category'],
                item['type']
            ]
            rows.append(row)
           
        return rows
    except Exception as e:
        print("error al cargar la informacion...")
