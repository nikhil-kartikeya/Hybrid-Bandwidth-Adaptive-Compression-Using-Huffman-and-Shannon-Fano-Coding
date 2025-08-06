# file_io.py
import pickle

def save_compressed_file(path, encoded_data, tree, shape):
    with open(path, 'wb') as f:
        pickle.dump((encoded_data, tree, shape), f)

def load_compressed_file(path):
    with open(path, 'rb') as f:
        return pickle.load(f)
