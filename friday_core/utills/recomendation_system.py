# recomendation_system.py

from collections import defaultdict, Counter
import json
from datetime import datetime, time

class RecomendationSystem:
  def __init__(self):
    self.user_habbits_file = "ml_models/user_habits.json"
    self.habits = self._load_habbits()

  def _load_habbits(self):
    try:
      with open(self.user_habbits_file, 'r', encoding='utf-8') as f:
        return json.load(f)
    except:
      return {
        'time_based_commands': defaultdict(Counter),
        'command_sequences': [],
        'favorite_actions': Counter()
      }
    
  def record_command(self, command, context=None):

    skip_commands =  ['пятница', "пят", 'выход', 'стоп', 'отдыхай', 'hitmo']
    skip_patterns = ['погода в', 'погода', 'температура']

    if not command or command.lower() in skip_commands:
      return
    
    if any(pattern in command.lower() for pattern in skip_patterns):
      return
      
    current_hour = datetime.now().hour
    time_slot = self._get_time_slot(current_hour)

    if time_slot not in self.habits['time_based_commands']:
      self.habits['time_based_commands'][time_slot] = {}

    if command not in self.habits['time_based_commands'][time_slot]:
      self.habits['time_based_commands'][time_slot][command] = 0

    self.habits['time_based_commands'][time_slot][command] += 1

    if 'last_command' in self.habits:
      sequence = (self.habits['last_command'], command)
      self.habits['command_sequences'].append(sequence)

    self.habits['last_command'] = command
    self._save_habits()

  def _get_time_slot(self, hour):
    if 5 <= hour < 12:
      return 'morning'
    elif 12 <= hour < 18:
      return 'afternoon'
    elif 18 <= hour < 23:
      return 'evening'
    else:
      return 'nignt'
    
  def get_recomendations(self, limit=3):
    current_slot = self._get_time_slot(datetime.now().hour)
    time_based_recs = self.habits['time_based_commands'].get(current_slot, {})

    recomendations = []

    sorted_commands = sorted(time_based_recs.items(), key=lambda x: x[1], reverse=True)

    for command, count in sorted_commands[:limit]:
      recomendations.append(f'Возможно вы хотите: {command}')

    if len(recomendations) < limit:
      general_recs = [
        "Узнать погоду",
        "Включить музыку", 
        "Проверить время",
        "Сделать скриншот"
      ]

      recomendations.extend(general_recs[:limit - len(recomendations)])

    return recomendations
  
  def _save_habits(self):
    try:
      with open(self.user_habbits_file, 'w', encoding='utf-8') as f:
        json.dump(self.habits, f, ensure_ascii=False, indent=2)
    except Exception as e:
      print(f'Ошибка сохранения привычек: {e}')

recomendation_system = RecomendationSystem()