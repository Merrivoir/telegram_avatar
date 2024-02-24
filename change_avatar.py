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

telegram_api_id = 21367964
telegram_api_hash = '990665185b0e0fb35005f475047797d3'

FONT_SIZE = 100
TEXT_Y_POSITION = 80

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

# create all avatars
for temperature in range(-99, 99):
    background_color = map_temperature_to_color(temperature, -25, 35)
    raw = Image.new('RGBA', (250, 250), background_color)
    parsed = ImageDraw.Draw(raw)
    length = len(str(temperature))
    if length == 1:
        x_start = 54
    if length == 2:
        x_start = 25
    if length == 3:
        x_start = 5

    font = ImageFont.truetype("FrozenCrystalAcademy.otf", FONT_SIZE)
    parsed.text((x_start, TEXT_Y_POSITION), f'{temperature}{celsius}', align="center", font=font)
    raw.save(f'{PATH}/{temperature}.png', "PNG")


""" def get_temperature(weather_data):
    return round(weather_data['main']['temp'])


def get_weather(location, api_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?id={location}&units=metric&appid={api_key}'
    r = requests.get(url)
    return r.json() """


""" client = TelegramClient('1', telegram_api_id, telegram_api_hash)
client.start()

last_temperature = -274

while True:
    weather_data = get_weather(location, openweather_api_key)
    temperature = get_temperature(weather_data)
    print(last_temperature, temperature)
    if temperature == last_temperature:
        time.sleep(15 * 60)
        continue

    client(DeletePhotosRequest(client.get_profile_photos('me')))
    file = client.upload_file(f'{PATH}/{temperature}.png')
    client(UploadProfilePhotoRequest(file))
    last_temperature = temperature
    time.sleep(15 * 60) """
