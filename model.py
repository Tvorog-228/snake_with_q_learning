import pickle
import os

def save_q_table(q_table, file_name='q_table.pkl'):
    folder_path = './model'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_name = os.path.join(folder_path, file_name)
    with open(file_name, 'wb') as f:
        pickle.dump(q_table, f)

def load_q_table(file_name='q_table.pkl'):
    file_name = os.path.join('./model', file_name)
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    return {}
