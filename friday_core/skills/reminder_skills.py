# friday_core/skills/reminder_skills.py

import threading
import time
from datetime import datetime, timedelta

class ReminderSkills:
    def __init__(self):
        self.reminders = []
        self.timers = []
    
    def set_reminder(self, text, minutes):
        """Установить напоминание"""
        reminder_time = datetime.now() + timedelta(minutes=minutes)
        self.reminders.append({
            'text': text,
            'time': reminder_time
        })
        
        # Запускаем таймер в отдельном потоке
        timer = threading.Timer(minutes * 60, self._trigger_reminder, [text])
        timer.start()
        self.timers.append(timer)
        
        return f"Напоминание установлено: '{text}' через {minutes} минут"
    
    def _trigger_reminder(self, text):
        """Срабатывание напоминания"""
        print(f"🔔 НАПОМИНАНИЕ: {text}")
        # Здесь можно добавить звуковое уведомление
    
    def set_timer(self, minutes):
        """Установить таймер"""
        timer = threading.Timer(minutes * 60, self._trigger_timer)
        timer.start()
        self.timers.append(timer)
        return f"Таймер установлен на {minutes} минут"
    
    def _trigger_timer(self):
        """Срабатывание таймера"""
        print("⏰ ТАЙМЕР: Время вышло!")
        # Можно добавить звук
    
    def get_reminders(self):
        """Показать активные напоминания"""
        if not self.reminders:
            return "Нет активных напоминаний"
        
        result = "Активные напоминания:\n"
        for i, reminder in enumerate(self.reminders, 1):
            time_left = reminder['time'] - datetime.now()
            minutes_left = int(time_left.total_seconds() / 60)
            result += f"{i}. {reminder['text']} (через {minutes_left} мин)\n"
        
        return result