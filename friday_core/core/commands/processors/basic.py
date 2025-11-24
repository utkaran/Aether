# friday_core/core/commands/processors/basic.py
from ..base import CommandProcessor, CommandContext

class BasicCommandProcessor(CommandProcessor):
    """Обработчик базовых команд"""
    
    def __init__(self, basic_skills, config):
        self.basic_skills = basic_skills
        self.config = config
        self._basic_keywords = [
            'время', 'час', 'времени', 'который час',
            'дата', 'число', 'какое число', 'сегодня',
            'сколько времени', 'привет', 'здравствуй'
        ]
    
    def can_handle(self, command: str) -> bool:
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in self._basic_keywords)
    
    def process(self, command: str, context: CommandContext) -> str:
        command_lower = command.lower()
        
        if any(word in command_lower for word in ["время", "час", "времени", "который час", "сколько времени"]):
            return self.basic_skills.get_time()
        elif any(word in command_lower for word in ["дата", "число", "какое число", "сегодня"]):
            return self.basic_skills.get_date()
        elif any(word in command_lower for word in ["привет", "здравствуй", "добрый", "хай"]):
            return "Здравствуйте! Чем могу помочь?"
        
        return "Базовая команда не распознана"