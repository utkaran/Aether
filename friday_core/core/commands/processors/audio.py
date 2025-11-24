# friday_core/core/commands/processors/audio.py
import re
from ..base import CommandProcessor, CommandContext

class AudioCommandProcessor(CommandProcessor):
    """Обработчик аудио команд"""
    
    def __init__(self, audio_skills):
        self.audio_skills = audio_skills
        self._audio_keywords = [
            'громкость', 'звук', 'тише', 'громче', 'максимум',
            'полная громкость', 'выключи звук', 'без звука', 'включи звук'
        ]
    
    def can_handle(self, command: str) -> bool:
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in self._audio_keywords)
    
    def process(self, command: str, context: CommandContext) -> str:
      command_lower = command.lower()
        
      if "громкость на" in command_lower:
            numbers = re.findall(r'\d+', command)
            if numbers:
                level = int(numbers[0])
                return self.audio_skills.set_volume(level)
            else:
                return "Укажите уровень: громкость на 50"
        
      elif "громкость максимум" in command_lower or "полная громкость" in command_lower:
        return self.audio_skills.set_volume(100)
      
      elif "тише" in command_lower:
        return self.audio_skills.volume_down()
      
      elif "громче" in command_lower:
        return self.audio_skills.volume_up()
      
      elif "выключи звук" in command_lower or "без звука" in command_lower:
        return self.audio_skills.mute()
      
      elif "включи звук" in command_lower:
        return self.audio_skills.set_volume(50)
      
      elif command_lower == "громкость":
        return "Скажите 'громче', 'тише', 'громкость на 50' или 'выключи звук'"
      
      return "Аудио команда не распознана"