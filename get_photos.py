import os
import io
from PIL import Image


def get_directory_path(folder_name: str) -> str:
    current_directory = os.getcwd()
    directory_path = os.path.join(current_directory, folder_name)
    if not os.path.isdir(directory_path):
        raise Exception(
            f'Папка {folder_name} не обнаружена в текущей директории')
    return directory_path


def compress_image(image_path: str, max_size_mb: int = 15) -> None:
    with Image.open(image_path) as image:
        image_byte_arr = io.BytesIO()
        image.save(image_byte_arr, format=image.format)
        current_size_mb = len(image_byte_arr.getvalue()) / (1024 * 1024)
        if current_size_mb >= max_size_mb:
            image.save(image_path, optimize=True, quality=85)


def find_images(folder_path: str) -> list:
    image_extensions = tuple(['.jpg', '.jpeg', '.png', '.gif'])
    image_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(image_extensions):
                image_path = os.path.join(root, file)
                compress_image(image_path=image_path)
                image_paths.append(image_path)
    return image_paths


def main(folder_name='default') -> list:

    folder_path = get_directory_path(folder_name)
    if not find_images(folder_path=folder_path):
        raise Exception('Папка пуста')
    return find_images(folder_path=folder_path)


if __name__ == "__main__":
    main()
