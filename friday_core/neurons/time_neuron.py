# friday_core/neurons/time_neuron.py

from friday_core.neurons.base_neuron import BaseNeuron

class TimeNeuron(BaseNeuron):

  def __init__(self):
    super().__init__('Временной нейрон')
    from friday_core.skills.basic_skills import BasicSkills
    self.basic_skills = BasicSkills()

  def can_handle(self, command: str) -> bool:
    time_keywords = [
      'время', 'час', 'времени', 'который час',
      'дата', 'число', 'какое число', 'сегодня',
      'сколько времени'
    ]
    command_lower = command.lower()
    return any(keyword in command_lower for keyword in time_keywords)
  
  def process(self, command: str) -> str:
    command_lower = command.lower()
    if any(word in command_lower for word in["время", "час", "времени", "который час", "сколько времени"]):
      return self.basic_skills.get_time()
    
    elif any(word in command_lower for word in["дата", "число", "какое число", "сегодня"]):
      return self.basic_skills.get_date()
    
    return 'Скажите "время" или "дата'