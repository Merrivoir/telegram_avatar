import os

id_main = os.getenv("api_id_main")
hash_main = os.getenv("api_hash_main")
id_sec = os.getenv("api_id_sec")
hash_sec = os.getenv("api_hash_sec")
weather_key = os.getenv("ow_api_key") 

print(f"Основной: {id_main}, хэш1: {hash_main}, Вторичный: {id_sec}, хэш2: {hash_sec}, Погода: {weather_key}")
