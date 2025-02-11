from pathlib import Path

def delete_non_images(folder_path):
    # Путь к папке
    folder = Path(folder_path)

    # Список допустимых расширений для изображений
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}

    # Проходим по всем файлам в папке
    for file in folder.iterdir():
        # Если это файл и его расширение не в списке допустимых, удаляем его
        if file.is_file() and file.suffix.lower() not in image_extensions:
            file.unlink()  # Удаление файла
    return file


def get_single_image_from_folder(folder_path):
    # Путь к папке
    folder = Path(folder_path)

    # Список допустимых расширений для изображений
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}

    # Проходим по всем файлам в папке
    for file in folder.iterdir():
        # Если это файл и его расширение в списке допустимых, возвращаем его
        if file.is_file() and file.suffix.lower() in image_extensions:
            return file 

    return None  # Возвращаем None, если изображение не найдено
