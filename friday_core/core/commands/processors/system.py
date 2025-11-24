# friday_core/core/commands/processors/system.py
import re
from ..base import CommandProcessor, CommandContext

class SystemCommandProcessor(CommandProcessor):
    """Обработчик системных команд"""
    
    def __init__(self, system_skills, config):
        self.system_skills = system_skills
        self.config = config
        self._system_keywords = [
            'выключи', 'перезагрузи', 'компьютер', 'система',
            'отмени выключение', 'перезагрузка', 'выключение'
        ]
    
    def can_handle(self, command: str) -> bool:
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in self._system_keywords)
    
    def process(self, command: str, context: CommandContext) -> str:
        command_lower = command.lower()
        
        if command_lower == 'отмени выключение':
            return self.system_skills.cancel_shutdown()
        
        elif "перезагрузи" in command_lower or "перезагрузка" in command_lower:
            numbers = re.findall(r'\d+', command)
            seconds = self.config.get('system.shutdown_timeout', 15)
            
            if numbers:
                seconds = int(numbers[0])
            
            return self.system_skills.restart(seconds)
        
        elif "выключи" in command_lower:
            numbers = re.findall(r'\d+', command)
            seconds = self.config.get('system.shutdown_timeout', 15)
            
            if numbers:
                seconds = int(numbers[0])
            
            if "компьютер" in command_lower or "пк" in command_lower:
                return self.system_skills.shutdown(seconds)
            else:
                return "Уточните: выключи компьютер или выключи через 10 секунд"
        
        return "Не понял системную команду"