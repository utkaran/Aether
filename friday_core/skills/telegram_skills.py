# telegram_skills.py
import requests
import json
import os
from pathlib import Path
from friday_core.config.config import config

class TelegramSkills:
    def __init__(self):
        self.token = config.get('telegram.bot_token', '')
        self.chat_id = config.get('telegram.chat_id', '')
    
    def setup_bot(self):
        """Проверяет настройку бота"""
        if not self.token:
            return "❌ Токен бота не настроен. Добавьте его в config.json в разделе telegram.bot_token"
        
        try:
            # Проверяем токен
            url = f"https://api.telegram.org/bot{self.token}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                config.set('telegram.enabled', True)
                return "✅ Бот настроен! Теперь получите chat_id командой 'получи айди телеграм'"
            else:
                config.set('telegram.enabled', False)
                return "❌ Неверный токен бота. Проверьте токен в config.json"
                
        except Exception as e:
            config.set('telegram.enabled', False)
            return f"❌ Ошибка проверки бота: {e}"
    
    def get_updates(self):
        """Получает обновления для получения chat_id"""
        if not config.get('telegram.enabled', False):
            return "❌ Сначала настройте бота: 'настрой телеграм'"
        
        try:
            url = f"https://api.telegram.org/bot{self.token}/getUpdates"
            print(f"🔍 Запрос к Telegram API: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f'Ответ от telegra: {data}')
                if data['ok'] and data['result']:
                    # Берем последнее сообщение
                    last_update = data['result'][-1]
                    chat_id = last_update['message']['chat']['id']
                    
                    # Сохраняем в конфиг
                    config.set('telegram.chat_id', str(chat_id))
                    self.chat_id = str(chat_id)
                    
                    return f"✅ Chat ID получен: {chat_id}. Теперь можно отправлять сообщения!"
                else:
                    return "❌ Отправьте сообщение боту в Telegram и повторите команду"
            else:
                return "❌ Ошибка получения обновлений. Проверьте токен бота."
                
        except Exception as e:
            return f"❌ Ошибка: {e}"
    
    def send_message(self, text):
        """Отправляет сообщение в Telegram"""
        if not config.get('telegram.enabled', False):
            return "❌ Telegram не настроен. Сначала выполните 'настрой телеграм'"
        
        if not self.chat_id:
            return "❌ Chat ID не получен. Выполните 'получи айди телеграм'"
        
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                return "✅ Сообщение отправлено в Telegram"
            else:
                error_msg = response.json().get('description', 'Неизвестная ошибка')
                return f"❌ Ошибка отправки: {error_msg}"
                
        except Exception as e:
            return f"❌ Ошибка отправки сообщения: {e}"
    
    def send_photo(self, photo_path, caption=""):
        """Отправляет фото в Telegram"""
        if not config.get('telegram.enabled', False) or not self.chat_id:
            return "❌ Telegram не настроен. Выполните 'настрой телеграм' и 'получи айди телеграм'"
        
        try:
            if not os.path.exists(photo_path):
                return f"❌ Файл не найден: {photo_path}"
            
            url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
            
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption
                }
                
                response = requests.post(url, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                return "✅ Фото отправлено в Telegram"
            else:
                error_msg = response.json().get('description', 'Неизвестная ошибка')
                return f"❌ Ошибка отправки фото: {error_msg}"
                
        except Exception as e:
            return f"❌ Ошибка отправки фото: {e}"
    
    def get_status(self):
        """Показывает статус настройки Telegram"""
        token_set = bool(config.get('telegram.bot_token'))
        chat_id_set = bool(config.get('telegram.chat_id'))
        enabled = config.get('telegram.enabled', False)
        
        status = "🔧 Статус Telegram:\n"
        status += f"🤖 Токен: {'✅ Установлен' if token_set else '❌ Не установлен'}\n"
        status += f"💬 Chat ID: {'✅ Получен' if chat_id_set else '❌ Не получен'}\n"
        status += f"🚀 Готовность: {'✅ Настроен' if enabled else '❌ Не настроен'}"
        
        if not token_set:
            status += "\n\n💡 Инструкция:\n"
            status += "1. Откройте config.json\n"
            status += "2. В разделе telegram добавьте:\n"
            status += '   "bot_token": "Your token"\n'
            status += "3. Перезапустите Пятницу"
        
        return status

# Глобальный экземпляр
telegram_skills = TelegramSkills()
