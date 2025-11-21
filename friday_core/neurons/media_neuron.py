# media_neuron.py

from friday_core.neurons.base_neuron import BaseNeuron

class MediaNeuron(BaseNeuron):
  def __init__(self):
    super().__init__('Медиа нейрон')
    self._media_skills = None

  def _get_media_skills(self):
    if self._media_skills is None:
      from friday_core.skills.media_skills import MediaKills
      self._media_skills = MediaKills
    return self._media_skills
  
  def can_handle(self, command: str) -> bool:
    media_keywords = [
      'музыка', 'включи', 'песня', 'hitmo', 'ютуб', 'youtube',
      'пауза', 'пауз', 'плэйлист', 'видео', 'медиа'
    ]

    command_lower = command.lower()
    return any(keyword in command_lower for keyword in media_keywords)
  
  def process(self, command: str) -> str:
    command_lower = command.lower()
    media_skills = self._get_media_skills()

    if 'включи музыку' in command_lower or 'hitmo' in command_lower:
      return media_skills.play_hitmo()
    elif 'включи youtube' in command_lower or 'включи ютуб' in command_lower:
      if 'включи youtube' in command_lower:
        query = command_lower.replace('включи youtube', '').strip()
        if query:
          return media_skills.play_on_youtube(query)
      return media_skills.play_on_youtube('тренды')
    
    elif 'пауза' in command_lower:
      return media_skills.pause_media()
    
    return 'Медиа команда не распознана'
