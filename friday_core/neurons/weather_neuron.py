# weather_neuron.py

from friday_core.neurons.base_neuron import BaseNeuron

class WeatherNeuron(BaseNeuron):
  def __init__(self):
    super().__init__('Погодный нейрон')

    from friday_core.skills.weather_skills import WeatherSkills
    self.weather_skills = WeatherSkills()

  def can_handle(self, command: str) -> bool:
    weather_keywords = [
      'погода', 'температура', 'градус', 'дождь', 'солнце',
      'на улице', 'мороз', 'жара', 'прогноз'
    ]

    command_lower = command.lower()
    return any(keyword in command_lower for keyword in weather_keywords)
  
  def process(self, command: str) -> str:
      command_lower = command.lower()

      if "в рязани" in command_lower or "рязань" in command_lower:
          weather_display = self.weather_skills.get_weather_for_display("Рязань")
          print(f"🌤️ {weather_display}")  # Выводим в консоль с эмодзи
          return self.weather_skills.get_weather("Рязань")
      elif "в москве" in command_lower or "москва" in command_lower:
          weather_display = self.weather_skills.get_weather_for_display("Москва")
          print(f"🌤️ {weather_display}")
          return self.weather_skills.get_weather("Москва")
      elif "в спб" in command_lower or "в питере" in command_lower or "санкт-петербург" in command_lower:
          weather_display = self.weather_skills.get_weather_for_display("Санкт-Петербург")
          print(f"🌤️ {weather_display}")
          return self.weather_skills.get_weather("Санкт-Петербург")
      elif "в казани" in command_lower or "казань" in command_lower:
          weather_display = self.weather_skills.get_weather_for_display("Казань")
          print(f"🌤️ {weather_display}")
          return self.weather_skills.get_weather("Казань")
      elif "в нижегород" in command_lower or "нижний новгород" in command_lower:
          weather_display = self.weather_skills.get_weather_for_display("Нижний Новгород")
          print(f"🌤️ {weather_display}")
          return self.weather_skills.get_weather("Нижний Новгород")
      elif "воронеж" in command_lower:
          weather_display = self.weather_skills.get_weather_for_display("Воронеж")
          print(f"🌤️ {weather_display}")
          return self.weather_skills.get_weather("Воронеж")
      elif "сочи" in command_lower:
          weather_display = self.weather_skills.get_weather_for_display("Сочи")
          print(f"🌤️ {weather_display}")
          return self.weather_skills.get_weather("Сочи")
      elif "екб" in command_lower or "екатеринбург" in command_lower:
          weather_display = self.weather_skills.get_weather_for_display("Екатеринбург")
          print(f"🌤️ {weather_display}")
          return self.weather_skills.get_weather("Екатеринбург")
      elif "новосибирск" in command_lower:
          weather_display = self.weather_skills.get_weather_for_display("Novosibirsk")
          print(f"🌤️ {weather_display}")
          return self.weather_skills.get_weather("Novosibirsk")
      elif "температура" in command_lower or "на улице" in command_lower:
          weather_display = self.weather_skills.get_weather_for_display()
          print(f"🌤️ {weather_display}")
          return self.weather_skills.get_weather_by_location()
      elif "краснодар" in command_lower:
          weather_display = self.weather_skills.get_weather_for_display("Krasnodar")
          print(f"🌤️ {weather_display}")
          return self.weather_skills.get_weather("Krasnodar")
      else:
          # Если просто "погода" - используем город из конфига
          weather_display = self.weather_skills.get_weather_for_display()
          print(f"🌤️ {weather_display}")
          return self.weather_skills.get_weather_by_location()