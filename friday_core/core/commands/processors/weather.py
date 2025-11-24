# friday_core/core/commands/processors/weather.py
from ..base import CommandProcessor, CommandContext

class WeatherCommandProcessor(CommandProcessor):
    """Обработчик погодных команд"""
    
    def __init__(self, weather_skills, config):
        self.weather_skills = weather_skills
        self.config = config
        self._weather_keywords = [
            'погода', 'температура', 'градус', 'дождь', 'солнце',
            'на улице', 'мороз', 'жара', 'прогноз'
        ]
    
    def can_handle(self, command: str) -> bool:
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in self._weather_keywords)
    
    def process(self, command: str, context: CommandContext) -> str:
        command_lower = command.lower()
        
        if "в рязани" in command_lower or "рязань" in command_lower:
            weather_display = self.weather_skills.get_weather_for_display("Рязань")
            print(f"🌤️ {weather_display}")
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
        elif "краснодар" in command_lower:
            weather_display = self.weather_skills.get_weather_for_display("Krasnodar")
            print(f"🌤️ {weather_display}")
            return self.weather_skills.get_weather("Krasnodar")
        elif "температура" in command_lower or "на улице" in command_lower:
            weather_display = self.weather_skills.get_weather_for_display()
            print(f"🌤️ {weather_display}")
            return self.weather_skills.get_weather_by_location()
        else:
            # Если просто "погода" - используем город из конфига
            weather_display = self.weather_skills.get_weather_for_display()
            print(f"🌤️ {weather_display}")
            return self.weather_skills.get_weather_by_location()