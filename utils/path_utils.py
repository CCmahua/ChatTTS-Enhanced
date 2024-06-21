import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


path_dict = {
    "OUTPUT_DIR": os.path.join(BASE_DIR, 'output_audio'),
    "CONFIG_DIR": os.path.join(BASE_DIR, 'data'),
}

def get_path(key):
    try:
        path = path_dict[key]
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path
    except KeyError:
        return f"Error: No path found for key '{key}'"


