# friday_core/neurons/reminder_neuron.py

from friday_core.neurons.base_neuron import BaseNeuron

class ReminderNeuron(BaseNeuron):
  def __init__(self):
    super().__init__('Нейрон напоминаний')
    self._reminder_skills = None

  def _get_reminder_skills(self):
    if self._reminder_skills is None:
      from friday_core.skills.reminder_skills import ReminderSkills
      self._reminder_skills = ReminderSkills
    return self._reminder_skills
  
  def can_handle(self, command: str) -> bool:
    reminder_keywords = [
      'напомни', 'таймер', 'напоминание', 'напоминай',
      'поставь таймер', 'поставить таймер'
    ]

    command_lower = command.lower()
    return any(keyword in command_lower for keyword in reminder_keywords)
  
  def process(self, command: str) -> str:
    command_lower = command.lower()
    reminder_skills = self._get_reminder_skills()

    if 'напомни' in command_lower and 'через' in command_lower:
      parts = command_lower.split('через')
      if len(parts) == 2:
        text = parts[0].replace('напомни', '').strip()
        time_part = parts[1].strip()
                
        import re
        minutes_match = re.search(r'(\d+)\s*минут', time_part)
        if minutes_match:
          minutes = int(minutes_match.group(1))
          return reminder_skills.set_reminder(text, minutes)
        
    elif 'таймер' in command_lower:
      time_match = re.search(r'таймер\s+на\s+(\d+)\s*минут', command_lower)
      if time_match:
        minutes = int(time_match.group(1))
        return reminder_skills.set_timer(minutes)
        
    return "Скажите: 'напомни позвонить через 10 минут' или 'поставь таймер на 5 минут'"
  