# friday_core/neurons/system_neuron.py
from .base_neuron import BaseNeuron
import re

class SystemNeuron(BaseNeuron):
    """Нейрон системных команд (выключение, перезагрузка)"""
    
    def __init__(self):
        super().__init__("Системный нейрон")
        self._system_skills = None
        self._config = None

    def _get_system_skills(self):
        if self._system_skills is None:
            from friday_core.skills.system_skills import SystemSkills
            self._system_skills = SystemSkills()
        return self._system_skills
    
    def _get_config(self):
        if self._config is None:
            from friday_core.config.config import config
            self._config = config
        return self._config
    
    def can_handle(self, command: str) -> bool:
        system_keywords = [
            'выключи', 'перезагрузи', 'компьютер', 'система',
            'отмени выключение', 'перезагрузка', 'выключение'
        ]
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in system_keywords)
    
    def process(self, command: str) -> str:
        command_lower = command.lower()
        
        if command_lower == 'отмени выключение':
            print('Отмена выключения...')
            return self.system_skills.cancel_shutdown()
        
        elif "перезагрузи" in command_lower or "перезагрузка" in command_lower:
            print("🔍 Обработка перезагрузки...")
            
            # Ищем время в команде
            numbers = re.findall(r'\d+', command)
            seconds = self.config.get('system.shutdown_timeout', 15)
            
            if numbers:
                seconds = int(numbers[0])
                print(f"🔍 Найдено время: {seconds} секунд")
            
            print(f"✅ Перезагрузка через {seconds} секунд!")
            return self.system_skills.restart(seconds)
        
        elif "выключи" in command_lower:
            print("🔍 Обработка выключения...")
            
            # Ищем время в команде
            numbers = re.findall(r'\d+', command)
            seconds = self.config.get('system.shutdown_timeout', 15)
            
            if numbers:
                seconds = int(numbers[0])
                print(f"🔍 Найдено время: {seconds} секунд")
            
            # Проверяем разные варианты команды
            if "компьютер" in command_lower or "пк" in command_lower:
                print(f"✅ Выключение через {seconds} секунд!")
                return self.system_skills.shutdown(seconds)
            else:
                # Если просто "выключи" без уточнения
                return "Уточните: выключи компьютер или выключи через 10 секунд"
        
        return "Не понял системную команду"