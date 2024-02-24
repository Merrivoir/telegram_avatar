from PIL import Image, ImageDraw, ImageFont

def interpolate_color(color1, color2, factor):
    # Функция для интерполяции цветов между двумя заданными цветами
    return (
        int(color1[0] * (1 - factor) + color2[0] * factor),
        int(color1[1] * (1 - factor) + color2[1] * factor),
        int(color1[2] * (1 - factor) + color2[2] * factor)
    )

def map_temperature_to_color(temperature, min_temp, max_temp):
    # Функция для отображения температуры в цвет фона
    # Определяем диапазон температур
    temperature_range = max_temp - min_temp
    # Находим фактор интерполяции в этом диапазоне
    factor = (temperature - min_temp) / temperature_range
    # Задаем начальный и конечный цвета
    start_color = (25, 120, 179)  # Синий
    end_color = (236, 81, 35)     # Красный
    # Интерполируем цвета
    interpolated_color = interpolate_color(start_color, end_color, factor)
    return interpolated_color

def generate_temperature_image(temperature, font_path="FrozenCrystalAcademy.otf", font_size=20, text_y_position=100, celsius="°C"):
    # Создаем изображение с заданным размером
    image = Image.new('RGBA', (250, 250), map_temperature_to_color(temperature, -100, 100))
    draw = ImageDraw.Draw(image)
    
    # Преобразуем температуру в строку
    temperature_str = str(temperature)
    
    # Определяем начальную позицию текста в зависимости от длины строки
    if len(temperature_str) == 1:
        x_start = 65
    elif len(temperature_str) == 2:
        x_start = 40
    else:
        x_start = 20
    
    # Загружаем шрифт
    font = ImageFont.truetype(font_path, font_size)
    
    # Рисуем текст на изображении
    draw.text((x_start, text_y_position), f'{temperature_str}{celsius}', fill=(255, 255, 255), align="center", font=font)
    
    return image

# Пример использования функции
temperature = -9
image = generate_temperature_image(temperature)
image.show()