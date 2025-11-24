# friday_core/neurons/screenshot_neuron.py

from friday_core.neurons.base_neuron import BaseNeuron

class ScreenshotNeuron(BaseNeuron):
  def __init__(self):
    super().__init__('Нейрон скриншотов')
    self._automation_skills = None

  def _get_automation_skills(self):
    if self._automation_skills is None:
      from friday_core.skills.automation_skills import automation_skills
      self._automation_skills = automation_skills
    return self._automation_skills
  
  def can_handle(self, command: str) -> bool:
    screenshot_keywords = [
      'скриншот', 'снимок', 'скрин', 'сними', 'сделай скриншот'
    ]
    command_lower = command.lower()
    return any(keyword in command_lower for keyword in screenshot_keywords)
  
  def process(self, command: str) -> str:
    command_lower = command.lower()
    automation_skills = self._get_automation_skills()
    import re

    if any(word in command_lower for word in ["покажи", "показать", "открой", "открыть", "последние"]):
        if "папк" in command_lower:
            return automation_skills.open_screenshots_folder()
        else:
            numbers = re.findall(r'\d+', command_lower)
            count = int(numbers[0]) if numbers else 5
            return automation_skills.list_recent_screenshots(count=count)
    
    elif any(word in command_lower for word in ["статистика", "сколько", "статус"]):
        return automation_skills.get_screenshots_stats()
    
    elif any(word in command_lower for word in ["удали", "очистки", "удалить", "очистить"]):
        numbers = re.findall(r'\d+', command_lower)
        days = int(numbers[0]) if numbers else 30
        return automation_skills.cleanup_old_screenshots(days=days)
    
    # Создание скриншотов
    numbers_map = {
        'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
        'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10
    }
    
    count = 1
    for word, num in numbers_map.items():
        if word in command_lower:
            count = num
            break
    else:
        numbers = re.findall(r'\d+', command_lower)
        if numbers:
            count = int(numbers[0])
    
    # Определяем тип скриншота
    if "области" in command_lower or "выдели" in command_lower:
        return automation_skills.take_screenshot(area=True)
    
    elif count > 1:
        return automation_skills.take_multiple_screenshots(count=count)
    
    else:
        description = ""
        if "с названием" in command_lower:
            description = command_lower.split("с названием")[-1].strip()
        elif "назови" in command_lower:
            description = command_lower.split("назови")[-1].strip()
        return automation_skills.take_screenshot(description=description)