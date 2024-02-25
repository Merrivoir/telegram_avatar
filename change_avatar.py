#!/usr/bin/env python
# -- coding: utf-8 --

from telethon import TelegramClient, sync
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
import requests
from PIL import ImageDraw, Image, ImageFont
import time

celsius = '°C'
PATH = 'temperature_images'

location = 1526384  # Almaty
openweather_api_key = 'c96076b2dcec72e588a42501bbb2f1ac'

telegram_api_id = 111111111
telegram_api_hash = '321321f32dsf3es51f32ae1f3as5e'

FONT_MAIN_SIZE = 90
FONT_ADD_SIZE = 40
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


def get_temperature(weather_data):
    return round(weather_data['main']['temp'])

def get_feels(weather_data):
    return round(weather_data['main']['feels_like'])


def get_weather(location, api_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?id={location}&units=metric&appid={api_key}'
    r = requests.get(url)
    r1 = {"coord":{"lon":76.95,"lat":43.25},"weather":[{"id":701,"main":"Mist","description":"mist","icon":"50d"}],"base":"stations","main":{"temp":266.1,"feels_like":261.18,"temp_min":266.1,"temp_max":266.1,"pressure":1030,"humidity":86},"visibility":1000,"wind":{"speed":3,"deg":340},"clouds":{"all":100},"dt":1708772797,"sys":{"type":1,"id":8818,"country":"KZ","sunrise":1708738694,"sunset":1708777992},"timezone":21600,"id":1526384,"name":"Almaty","cod":200}
    return r.json()

def generate_temperature_image(temperature, feels):
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
    font_main = ImageFont.truetype("FrozenCrystalAcademy.otf", FONT_MAIN_SIZE)
    font_add = ImageFont.truetype("FrozenCrystalAcademy.otf", FONT_ADD_SIZE)
    
    # Рисуем текст на изображении
    draw.text((x_start, TEXT_Y_POSITION), f'{temperature}{celsius}', align="center", font=font_main)
    draw.text((x_start + 54, TEXT_ADD_Y_POSITION), f'{feels}{celsius}', align="center", font=font_add)
    
    image.save(f'temp.png', "PNG")

client = TelegramClient('1', telegram_api_id, telegram_api_hash)
client.start()

last_temperature = -274

while True:

    weather_data = get_weather(location, openweather_api_key)
    temperature = get_temperature(weather_data)
    feels = get_feels(weather_data)
    
    print(last_temperature, temperature, feels)
    
    if temperature == last_temperature:
        time.sleep(15 * 60)
        continue
    
    generate_temperature_image(temperature, feels)
    
    client(DeletePhotosRequest(client.get_profile_photos('me')))
    temper = client.upload_file(f'temp.png')
    
    client(UploadProfilePhotoRequest(file=temper))
    last_temperature = temperature
    
    time.sleep(15 * 60)
