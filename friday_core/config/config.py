"""
Конфигурация голосового ассистента Пятница
"""
# config.py

import os
import json
from pathlib import Path

class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.default_config = {
            # 🔧 Основные настройки
            "assistant": {
                "name": "Пятница",
                "language": "ru-RU",
                "wake_words": ["пятница", "пят"],
                "response_delay": 0.5
            },
            
            # 🎤 Голосовые настройки
            "voice": {
            "rate": 150,
            "volume": 1.0,
            "voice_id": None,
            "edge_voice": "ru-RU-SvetlanaNeural",  # Добавьте эту строку
            "tts_provider": "edge"  # И эту
            },
            
            # 🌐 API ключи
            "api_keys": {
                "openweathermap": "d6949ae5f1fc1c5209f7d26b2044e215",
                "yandex_speech": ""  # для будущего использования
            },
            
            # 🗺️ Геолокация
            "location": {
                "default_city": "Рязань",
                "timezone": "Europe/Moscow"
            },
            
            # 🔊 Звуковые настройки
            "sounds": {
                "enabled": True,
                "volume": 0.5
            },
            
            # 🎵 Медиа настройки
            "media": {
                "default_music_service": "youtube",
                "browser": "default"
            },
            
            # ⚙️ Системные настройки
            "system": {
                "shutdown_timeout": 15,
                "auto_update": False
            },
            #Telegram
            "telegram": {
            "bot_token": "7267509799:AAGPnUMg5G47eNRCaipVyTbhleyxh6LRDno",  # Токен бота
            "chat_id": "",    # ID чата
            "enabled": False  # Включен ли Telegram
    },
        }
        
        self.config = self.load_config()
    
    def load_config(self):
        """Загружает конфигурацию из файла или создает новую"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Объединяем с дефолтными настройками
                    return self.merge_configs(self.default_config, loaded_config)
            else:
                # Создаем файл с настройками по умолчанию
                self.save_config(self.default_config)
                return self.default_config.copy()
                
        except Exception as e:
            print(f"❌ Ошибка загрузки конфигурации: {e}")
            return self.default_config.copy()
    
    def merge_configs(self, default, user):
        """Рекурсивно объединяет конфигурации"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_configs(result[key], value)
            else:
                result[key] = value
                
        return result
    
    def save_config(self, config=None):
        """Сохраняет конфигурацию в файл"""
        try:
            if config is None:
                config = self.config
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения конфигурации: {e}")
            return False
    
    def get(self, key_path, default=None):
        """Получает значение по пути ключа"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path, value):
        """Устанавливает значение по пути ключа"""
        keys = key_path.split('.')
        config_ref = self.config
        
        for key in keys[:-1]:
            if key not in config_ref:
                config_ref[key] = {}
            config_ref = config_ref[key]
        
        config_ref[keys[-1]] = value
        self.save_config()
    
    def reset_to_defaults(self):
        """Сбрасывает настройки к значениям по умолчанию"""
        self.config = self.default_config.copy()
        self.save_config()
        return "Настройки сброшены к значениям по умолчанию"

# Глобальный экземпляр конфигурации
config = Config()