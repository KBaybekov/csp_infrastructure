from utils import save_structure_to_yaml

# Задайте путь к директории и к файлу для вывода
directory_path = '/mnt/cephfs8_ro/nanopore/'
output_yaml_file = '/home/PAK-CSPMZ/kbajbekov/nanopore/nanopore_dir_structure.yaml'

save_structure_to_yaml(directory_path, output_yaml_file)