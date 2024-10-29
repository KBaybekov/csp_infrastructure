import os
import yaml

def get_folder_structure(directory: str) -> dict:
    """
    Рекурсивно обходит папки и файлы, создавая структуру словаря.
    
    :param directory: Путь к директории, которую нужно проанализировать
    :return: Словарь с отображением структуры папок и файлов
    """
    structure = {}
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            structure[item] = get_folder_structure(item_path)  # Рекурсивный вызов для подкаталогов
        else:
            structure[item] = None  # Файл
    return structure

def save_structure_to_yaml(directory: str, output_file: str):
    """
    Сохраняет структуру папки в YAML-файл.
    
    :param directory: Путь к директории, которую нужно проанализировать
    :param output_file: Путь к YAML-файлу, куда будет сохранена структура
    """
    structure = get_folder_structure(directory)
    with open(output_file, 'w') as yaml_file:
        yaml.dump(structure, yaml_file, default_flow_style=False, sort_keys=False)