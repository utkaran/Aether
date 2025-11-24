"""
Система персонализации для Пятницы
Запоминает предпочтения пользователя и адаптируется под него
"""
# friday_core/config/personalization.py

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
import pickle

class Personalization:
    def __init__(self):
        self.profile_file = "data/user_profile.json"
        self.habits_file = "data/user_habits.pkl"
        self._ensure_data_dir()
        self.user_profile = self._load_profile()
        self.user_habits = self._load_habits()
        
        # Статистика использования
        self.command_stats = defaultdict(int)
        self.time_preferences = defaultdict(lambda: defaultdict(int))
        
        print("🎯 Система персонализации инициализирована")
    
    def _ensure_data_dir(self):
        """Создает папку data если её нет"""
        Path("data").mkdir(exist_ok=True)
    
    def _load_profile(self):
        """Загружает профиль пользователя"""
        default_profile = {
            "name": "Сэр",
            "preferences": {
                "voice_speed": 150,
                "voice_volume": 80,
                "favorite_voice": "ru-RU-SvetlanaNeural",
                "wake_word": "пятница",
                "response_style": "professional",  # professional, casual, friendly
                "time_format": "24h",  # 24h or 12h
                "temperature_unit": "celsius"  # celsius or fahrenheit
            },
            "favorites": {
                "cities": ["Рязань", "Москва"],
                "music_services": ["youtube"],
                "browsers": ["chrome"],
                "applications": ["notepad", "calculator"]
            },
            "schedule": {
                "wake_up_time": "08:00",
                "sleep_time": "23:00",
                "work_hours": ["09:00", "18:00"]
            },
            "created_at": datetime.now().isoformat(),
            "last_used": datetime.now().isoformat()
        }
        
        try:
            if os.path.exists(self.profile_file):
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                    # Объединяем с дефолтными настройками
                    return self._merge_profiles(default_profile, profile)
            return default_profile
        except Exception as e:
            print(f"❌ Ошибка загрузки профиля: {e}")
            return default_profile
    
    def _load_habits(self):
        """Загружает привычки пользователя"""
        try:
            if os.path.exists(self.habits_file):
                with open(self.habits_file, 'rb') as f:
                    return pickle.load(f)
            return {
                "frequent_commands": Counter(),
                "time_patterns": defaultdict(Counter),
                "context_preferences": {},
                "conversation_history": []
            }
        except Exception as e:
            print(f"❌ Ошибка загрузки привычек: {e}")
            return {
                "frequent_commands": Counter(),
                "time_patterns": defaultdict(Counter),
                "context_preferences": {},
                "conversation_history": []
            }
    
    def _merge_profiles(self, default, user):
        """Рекурсивно объединяет профили"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_profiles(result[key], value)
            else:
                result[key] = value
                
        return result
    
    def save_profile(self):
        """Сохраняет профиль пользователя"""
        try:
            self.user_profile["last_used"] = datetime.now().isoformat()
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_profile, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения профиля: {e}")
            return False
    
    def save_habits(self):
        """Сохраняет привычки пользователя"""
        try:
            with open(self.habits_file, 'wb') as f:
                pickle.dump(self.user_habits, f)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения привычек: {e}")
            return False
    
    def update_usage_statistics(self, command, context=None):
        """Обновляет статистику использования"""
        try:
            # Увеличиваем счетчик команды
            self.user_habits["frequent_commands"][command] += 1
            
            # Записываем временной паттерн
            current_hour = datetime.now().strftime("%H:00")
            self.user_habits["time_patterns"][current_hour][command] += 1
            
            # Сохраняем контекст если предоставлен
            if context:
                self.user_habits["conversation_history"].append({
                    "timestamp": datetime.now().isoformat(),
                    "command": command,
                    "context": context
                })

                if len(self.user_habits['conversation_history']) > 100:
                    self.user_habits['conversation_history'] = self.user_habits['conversation_history'][-100:]

            if sum(self.user_habits['frequent_commands'].values()) % 10 == 0:
                self.user_habits

        except Exception as e:
            print(f'Ошибка обновления статистики: {e}')

    def get_user_name(self):
        return self.user_profile.get('name', 'Сэр')
    
    def set_user_name(self, name):
        self.user_profile['name'] = name
        self.save_profile()
        return f'Теперь я буду обращаться к вам: {name}'
    
    def get_personalized_greeting(self):
        name = self.get_user_name()
        current_hour = datetime.now().hour

        if 5 <= current_hour < 12:
            greeting = f'Доброе утро, {name}'
        elif 12 <= current_hour < 18:
            greeting = f'Добрый день, {name}'
        elif 18 <= current_hour <23:
            greeting = f'Добрый вечер, {name}'
        else:
            greeting = f'Доброй ночи, {name}'

        most_common = self.user_habits['frequent_commands'].most_common(1)
        if most_common:
            command, count = most_common[0]
            if 'погода' in command.lower():
                greeting += ". Сегодня проверю погоду для вас?"
            elif 'музыка' in command.lower():
                greeting += ". Включить вашу любимую музыку?"
            elif 'время' in command.lower():
                greeting += ". Нужно узнать текущее время?"

        return greeting
    
    def get_response_style(self):
        return self.user_profile['preferences'].get('response_style', 'professional')
    
    def set_response_style(self,style):
        valid_styles = ["professional", "casual", "friendly"]
        if style in valid_styles:
            self.user_profile["preferences"]["response_style"] = style
            self.save_profile()
            return f'Стиль ответов изменен на : {style}'
        else:
            return f"❌ Доступные стили: {', '.join(valid_styles)}"
        
    def get_favorite_city(self):
        favorites = self.user_profile['favorites'].get('cities', [])
        return favorites[0] if favorites else 'Рязань'
    
    def add_favorite_city(self, city):
        if city not in self.user_profile['favorites']['cities']:
            self.user_profile['favorites']['cities'].append(city)
            self.save_profile()
            return f"✅ Город {city} добавлен в избранное"
        return f"✅ Город {city} уже в избранном"
    
    def get_frequent_commands(self, limit=5):
        return self.user_habits['frequent_commands'].most_common(limit)
    
    def get_time_based_suggestions(self):
        current_hour = datetime.now().hour
        current_time = datetime.now().strftime("%H:00")

        time_patterns = self.user_habits['time_patterns'].get(current_time, {})

        suggestions = []
        
        if 6 <= current_hour <10:
            suggestions.extend(['погода', 'новости', 'план на день'])
        elif 10 <= current_hour <18:
            suggestions.extend('таймер', 'напоминание', 'открыть браузер')
        elif 18 <= current_hour < 23:
            suggestions.extend('музыка', 'фильм', 'выключить компьютер')

        for command, count in time_patterns.most_common(3):
            if command not in suggestions:
                suggestions.append(command)

        return suggestions[:5]
    def learn_from_conservation(self, user_input, assistant_response):
        try:
            friendly_words = ['спасибо', "пожалуйста", "отлично", "хорошо"]
            if any(word in user_input.lower() for word in friendly_words):
                if self.user_profile['preferences']['response_style'] == 'proffesional':
                    self.user_profile['prefences']['response_style'] = 'friendly'

            if 'погода' in user_input.lower():
                self.user_habits['context_preferences']['checks_weather_often'] == True

            self.save_profile()
            self.save_habits()

        except Exception as e:
            print(f'Ошибка обучения: {e}')

    def get_personalized_help(self):
        name = self.get_user_name()
        frequent_commands = self.get_frequent_commands(3)
        suggestions = self.get_time_based_suggestions()

        help_text = f'''
        Персонализированная помощь для {name.upper()}
Ваши частые команды: 
'''
        for i, (command, count) in enumerate(frequent_commands, 1):
            help_text += f'    {i}. {command} ({count} раз)\n'

        help_text += f'''
        Предложения сейчас:
''' 
        for i , suggestion in enumerate(suggestions, 1):
            help_text += f'   {i}. {suggestion}\n'

        help_text += f'''
        Ваши настройки:
        Стиль общения: {self.get_response_style()}
        Любимый город: {self.get_favorite_city()}
        Имя: {name}

Скажите "изменить настройки" для персонализации
'''
        return help_text

personalization = Personalization()


        
      