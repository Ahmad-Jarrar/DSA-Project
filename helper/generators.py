import os
from config import DATA_PATH


def dataset_files():
    for subdir, _, files in os.walk(DATA_PATH):
        
        subdir_path = os.path.abspath(subdir)

        for f in files:
            yield os.path.join(subdir_path, f)

def test():
    file_names = []
    for file in dataset_files():
        print(file)
        file_names.append(file)

    print(len(file_names))

if __name__ == "__main__":
    test()