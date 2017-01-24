import pickle

DATA_FILE = "characters_data"


def read_data_file():
    try:
        with open(DATA_FILE, 'rb') as f:
            return pickle.load(f)
    except IOError:
        return []


def create_and_save_data(name, info):
    info_about_character = {
        name: info
    }
    data = read_data_file()
    data.append(info_about_character)
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(data, f)

for _ in range(6):
    name = input("name")
    info = input("info")
    create_and_save_data(name, info)

