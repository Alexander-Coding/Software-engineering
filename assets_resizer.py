import os
from PIL import Image

def process_images(input_folder):
    # Проходим по всем подпапкам и файлам в указанной папке
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.png'):
                file_path = os.path.join(root, file)
                # Открываем изображение
                with Image.open(file_path) as img:
                    # Преобразуем изображение в режим RGBA, чтобы учесть прозрачность
                    img = img.convert("RGBA")
                    # Получаем размеры изображения
                    bbox = img.getbbox()  # Получаем bounding box без пустых пикселей
                    if bbox:
                        # Обрезаем изображение по границам непустого фона
                        img_cropped = img.crop(bbox)
                        img_cropped.save(file_path)
                        # Масштабируем до 32x32 пикселей
                        #img_resized = img_cropped.resize((32, 32), Image.LANCZOS)
                        # Сохраняем изображение, перезаписывая исходное
                        #img_resized.save(file_path)
                        print(f"Обработано: {file_path}")


if __name__ == "__main__":
    # Укажите путь к папке с изображениями
    input_folder = r"C:\Users\Alexa\github\BioSense\mario\assets\images"
    process_images(input_folder)
