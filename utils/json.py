from json import load, dump

def get_data(file):
    with open(file, 'r') as file_data:
        data = load(file_data)
    return data