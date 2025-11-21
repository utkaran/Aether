import requests
import json
import re
import time
from friday_core.config.config import config

class WeatherSkills:
    def __init__(self):
        self.api_key = config.get('api_keys.openweathermap', 'Your API')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.default_city = config.get('location.default_city', 'Рязань')
        self.cache = {}
        self.cache_timeout = 600  # 10 минут

    def get_weather(self, city=None):
        if city is None:
            city = self.default_city
            
        # Проверяем кэш
        cache_key = city.lower()
        current_time = time.time()
        if (cache_key in self.cache and 
            current_time - self.cache[cache_key]['timestamp'] < self.cache_timeout):
            print(f"🌤️ Использую кэшированные данные для {city}")
            return self.cache[cache_key]['data']
        
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'ru'
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()

            if response.status_code == 200:
                temperature = data['main']['temp']
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                feels_like = data['main']['feels_like']

                emoji = self._get_weather_emoji(description)
                
                # Текст для вывода в консоли (с эмодзи)
                console_text = (f"{emoji} В городе {city}: {description}\n"
                               f" Температура: {round(temperature)}°C (ощущается как {round(feels_like)}°C)\n"
                               f" Влажность: {humidity}%\n"
                               f" Ветер: {wind_speed} м/с")
                
                # Текст для озвучки (без эмодзи)
                speech_text = (f"В городе {city}: {description}. "
                              f"Температура: {round(temperature)} градусов. "
                              f"Ощущается как {round(feels_like)} градусов. "
                              f"Влажность: {humidity} процентов. "
                              f"Ветер: {wind_speed} метров в секунду")
                
                # Сохраняем в кэш
                self.cache[cache_key] = {
                    'data': speech_text,
                    'timestamp': current_time
                }
                
                return speech_text  # Возвращаем текст без эмодзи для озвучки
                
            else:
                error_msg = f"Не удалось получить погоду для {city}. Проверь название города."
                return error_msg
            
        except requests.Timeout:
            return "Таймаут при получении погоды. Проверьте интернет-соединение."
        except requests.RequestException as e:
            return f"Ошибка сети при получении погоды: {e}"
        except Exception as e:
            return f"Ошибка получения погоды: {e}"
    
    def get_weather_for_display(self, city=None):
        """Получить погоду для отображения в консоли (с эмодзи)"""
        if city is None:
            city = self.default_city
            
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'ru'
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()

            if response.status_code == 200:
                temperature = data['main']['temp']
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                feels_like = data['main']['feels_like']

                emoji = self._get_weather_emoji(description)
                
                # Текст для вывода в консоли (с эмодзи)
                return (f"{emoji} В городе {city}: {description}\n"
                        f"🌡 Температура: {round(temperature)}°C (ощущается как {round(feels_like)}°C)\n"
                        f"💧 Влажность: {humidity}%\n"
                        f"💨 Ветер: {wind_speed} м/с")
                
            else:
                return f"❌ Не удалось получить погоду для {city}. Проверь название города."
            
        except Exception as e:
            return f"❌ Ошибка получения погоды: {e}"

    def _get_weather_emoji(self, description):
        emoji_map = {
            'ясно': '☀️',
            'солнечно': '☀️',
            'облачно': '⛅',
            'пасмурно': '☁️',
            'дождь': '🌧️',
            'небольшой дождь': '🌦️',
            'снег': '❄️',
            'туман': '🌫️',
            'гроза': '⛈️',
            'переменная облачность': '🌤️'
        }
        
        for key, emoji in emoji_map.items():
            if key in description.lower():
                return emoji
        return '🌡️'
    
    def get_weather_by_location(self):
        return self.get_weather(self.default_city)
