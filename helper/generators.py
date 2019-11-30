import os
from config import DATA_PATH


def files():
    for subdir, _, files in os.walk(DATA_PATH):
        
        subdir_path = os.path.abspath(subdir)

        for f in files[:2000]:
            yield os.path.join(subdir_path, f)

if __name__ == "__main__":
    
    file_names = []
    for file in files():
        print(file)
        file_names.append(file)

    print(len(file_names))