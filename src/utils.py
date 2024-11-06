import os
import yaml


def get_fast5_files(dir:str) -> dict:
    subdirs = [os.path.join(dir, s) for s in os.listdir(dir) if os.path.isdir(os.path.join(dir, s, ))]
    sample_data = {}
    for subdir in subdirs:
        fast5s = []
        for root, _ds, fs in os.walk(subdir):
            for f in fs:
                if f.endswith('.fast5') and os.path.basename(root) == 'fast5_pass':
                    fast5s.append(os.path.join(root, f))
        if fast5s:
            sample_data[os.path.basename(subdir)] = fast5s
    if not sample_data:
        raise FileNotFoundError('FAST5 файлы не найдены!')
    return sample_data







    files = [os.path.join(dir, s) for s in os.listdir(dir) if os.path.isdir({os.path.join(dir, s, )}) and os.path]
    if not files:
        raise FileNotFoundError("Образцы не найдены. Проверьте входные и исключаемые образцы, а также директорию с исходными файлами.")
    return files

def get_samples_in_dir(dir:str, extensions:tuple):
    """
    Генерирует список файлов на основе включающих и исключающих образцов.
    Выдаёт ошибку, если итоговый список пустой.

    :param dir: Директория, где искать файлы.
    :param extensions: Расширения файлов для поиска.
    :return: Список путей к файлам.
    """
    # Ищем все файлы в директории с указанными расширениями
    files = [os.path.join(dir, s) for s in os.listdir(dir) if s.endswith(extensions)]
    if not files:
        raise FileNotFoundError("Образцы не найдены. Проверьте входные и исключаемые образцы, а также директорию с исходными файлами.")
    return files


def get_samples_in_dir_tree(dir:str, extensions:tuple) -> list:
    """
    Генерирует список файлов, проходя по дереву папок, корнем которого является dir.
    Выдаёт ошибку, если итоговый список пустой.

    :param dir: Директория, где искать файлы.
    :param extensions: Кортеж расширений файлов для поиска.
    :return: Список файлов с путями.
    """
    files = []
    for root, _ds, fs in os.walk(dir):
        samples = [os.path.join(root, f) for f in fs 
                    if f.endswith(extensions)]
        files.extend(samples)
    if not files:
        raise FileNotFoundError("Образцы не найдены. Проверьте входные и исключаемые образцы, а также директорию с исходными файлами.")
    return files

def save_yaml(filename, path, data):
    """
    Сохраняет словарь в файл в формате YAML.
    
    :param filename: Имя файла для сохранения (например, 'config.yaml')
    :param path: Путь к директории, где будет сохранён файл
    :param data: Словарь с данными, которые нужно сохранить в YAML
    """
    # Полный путь к файлу
    file_path = f'{path}{filename}.yaml'

    # Записываем данные в YAML-файл
    with open(file_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False, sort_keys=False)