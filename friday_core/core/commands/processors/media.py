# friday_core/core/commands/processors/media.py
from ..base import CommandProcessor, CommandContext

class MediaCommandProcessor(CommandProcessor):
    """Обработчик медиа команд"""
    
    def __init__(self, media_skills):
        self.media_skills = media_skills
        self._media_keywords = [
            'музыка', 'включи', 'песня', 'hitmo', 'ютуб', 'youtube',
            'пауза', 'пауз', 'плэйлист', 'видео', 'медиа'
        ]
    
    def can_handle(self, command: str) -> bool:
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in self._media_keywords)
    
    def process(self, command: str, context: CommandContext) -> str:
        command_lower = command.lower()

        if 'включи музыку' in command_lower or 'hitmo' in command_lower:
            return self.media_skills.play_hitmo()
        elif 'включи youtube' in command_lower or 'включи ютуб' in command_lower:
            if 'включи youtube' in command_lower:
                query = command_lower.replace('включи youtube', '').strip()
                if query:
                    return self.media_skills.play_on_youtube(query)
            return self.media_skills.play_on_youtube('тренды')
        elif 'пауза' in command_lower:
            return self.media_skills.pause_media()
        
        return 'Медиа команда не распознана'