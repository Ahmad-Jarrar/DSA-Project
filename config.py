import os
import shutil

PROJECT_PATH = os.getcwd()


# Give the path of your dataset
DATA_PATH = os.path.join(PROJECT_PATH, 'Data')

# internal Files
FILES_PATH = os.path.join(PROJECT_PATH, 'Storage')
LEXICON_PATH = os.path.join(FILES_PATH, 'lexicon.json')
BARRELS_PATH = os.path.join(FILES_PATH, 'barrels')
EXTRA_PATH = os.path.join(FILES_PATH, 'extra')


NO_OF_THREADS = 8
NO_OF_BARRELS = 64
BARREL_CAPACITY = 8000

def clean_project():
    try:
        shutil.rmtree(FILES_PATH, ignore_errors=True)
    except:
        pass

    try:
        shutil.rmtree(EXTRA_PATH, ignore_errors=True)
    except:
        pass

    try:
        shutil.rmtree(BARRELS_PATH, ignore_errors=True)
    except:
        pass

def build_paths():

    try:
        os.stat(FILES_PATH)
    except:
        os.mkdir(FILES_PATH)
    
    try:
        os.stat(BARRELS_PATH)
    except:
        os.mkdir(BARRELS_PATH)

    try:
        os.stat(EXTRA_PATH)
    except:
        os.mkdir(EXTRA_PATH)
