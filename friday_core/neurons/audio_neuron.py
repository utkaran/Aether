# audio_neuron.py

from friday_core.neurons.base_neuron import BaseNeuron

class AudioNeuro(BaseNeuron):
  def __init__(self):
    super().__init__('Аудио нейрон')
    self._audio_skills = None

  def _get_audio_skills(self):
    if self._audio_skills is None:
      from friday_core.skills.audio_skills import AudioSkills
      self._audio_skills = AudioSkills
    return self._audio_skills
  
  def can_handle(self, command: str) -> bool:
    audio_keywords = [
      'громкость', 'звук', 'тише', 'громче', 'максимум',
      'полная громкость', 'выключи звук', 'без звука', 'включи звук'
    ]

    command_lower = command.lower()
    return any(keyword in command_lower for keyword in audio_keywords)
  
  def process(self, command: str) -> str:
    command_lower = command.lower()
    audio_skills = self._get_audio_skills()

    if "громкость на" in command_lower:
        import re
        numbers = re.findall(r'\d+', command)
        if numbers:
            level = int(numbers[0])
            return audio_skills.set_volume(level)
        else:
            return "Укажите уровень: громкость на 50"
    
    elif "громкость максимум" in command_lower or "полная громкость" in command_lower:
        return audio_skills.set_volume(100)
    
    elif "тише" in command_lower:
        return audio_skills.volume_down()
    
    elif "громче" in command_lower:
        return audio_skills.volume_up()
    
    elif "выключи звук" in command_lower or "без звука" in command_lower:
        return audio_skills.mute()
    
    elif "включи звук" in command_lower:
        return audio_skills.set_volume(50)
    
    elif command_lower == "громкость":
        return "Скажите 'громче', 'тише', 'громкость на 50' или 'выключи звук'"
    
    return "Аудио команда не распознана"