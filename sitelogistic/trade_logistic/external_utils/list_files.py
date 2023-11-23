def list_files(directory: str) -> dict:
    """Эта функция перебирает файлы в каталоге и выводит их имена и первые строки.
    Параметры: directory - имя каталога, в котором хотим перебрать файлы
    Возвращает: None
    """
    import os

    file_dict = {}
    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if first_line:
                file_dict[first_line] = file_path

    return file_dict
