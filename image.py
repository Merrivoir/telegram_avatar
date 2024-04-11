from PIL import Image, ImageDraw, ImageFont

celsius = '°C'

location = 1526384  # Almaty
openweather_api_key = 'c96076b2dcec72e588a42501bbb2f1ac'

telegram_api_id = 21367964
telegram_api_hash = '990665185b0e0fb35005f475047797d3'

FONT_MAIN_SIZE = 90
FONT_ADD_SIZE = 48
TEXT_Y_POSITION = 55
TEXT_ADD_Y_POSITION = 160

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

def generate_temperature_image(temperature, feels):
    # Создаем изображение с заданным размером
    image = Image.new('RGBA', (250, 250), map_temperature_to_color(temperature, -20, 20))
    draw = ImageDraw.Draw(image)
    
    # Преобразуем температуру в строку
    temperature_str = str(temperature), str(feels)
    
    # Определяем начальную позицию текста в зависимости от длины строки
    if len(temperature_str[0]) == 1:
        x_start = 65
    elif len(temperature_str[0]) == 2:
        x_start = 40
    else:
        x_start = 20
    
    # Загружаем шрифт
    font_main = ImageFont.truetype("FrozenCrystalAcademy.otf", FONT_MAIN_SIZE)
    font_add = ImageFont.truetype("FrozenCrystalAcademy.otf", FONT_ADD_SIZE)
    
    # Рисуем текст на изображении
    draw.text((x_start, TEXT_Y_POSITION), f'{temperature}{celsius}', align="center", font=font_main)
    draw.text((12, TEXT_ADD_Y_POSITION), f'{feels}{celsius} mist', align="center", font=font_add)
    
    image.save(f'temp-a.png', "PNG")