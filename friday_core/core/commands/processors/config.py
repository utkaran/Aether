# friday_core/core/commands/processors/config.py
import re
from ..base import CommandProcessor, CommandContext

class ConfigCommandProcessor(CommandProcessor):
    """Обработчик команд конфигурации"""
    
    def __init__(self, config):
        self.config = config
        self._config_keywords = [
            'настройки', 'конфиг', 'сброс', 'город', 'голос',
            'громкость речи', 'скорость речи', 'время выключения'
        ]
    
    def can_handle(self, command: str) -> bool:
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in self._config_keywords)
    
    def process(self, command: str, context: CommandContext) -> str:
        command_lower = command.lower()
        
        if "покажи настройки" in command_lower:
            current_city = self.config.get('location.default_city', 'Рязань')
            speech_speed = self.config.get('voice.rate', 150)
            shutdown_timeout = self.config.get('system.shutdown_timeout', 15)
            
            return f"""
📋 ТЕКУЩИЕ НАСТРОЙКИ:
🏙️ Город: {current_city}
🎤 Скорость речи: {speech_speed}
⏰ Время выключения: {shutdown_timeout} сек
"""
        
        elif "измени город" in command_lower:
            city = command_lower.replace("измени город", "").strip()
            if city:
                self.config.set('location.default_city', city)
                return f"Город по умолчанию изменен на {city}"
        
        elif "скорость речи" in command_lower:
            numbers = re.findall(r'\d+', command)
            if numbers:
                speed = max(50, min(300, int(numbers[0])))
                self.config.set('voice.rate', speed)
                return f"Скорость речи установлена на {speed}"
        
        return "Команда конфигурации не распознана"