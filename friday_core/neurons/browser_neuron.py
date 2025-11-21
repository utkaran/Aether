# browser_neuron.py

from friday_core.neurons.base_neuron import BaseNeuron

class BrowserNeuron(BaseNeuron):
  def __init__(self):
    super().__init__('Нейрон браузеров и приложений')

    self._basic_skills = None
    self._automation_skills = None

  def _get_basic_skills(self):
    if self._basic_skills is None:
      from friday_core.skills.basic_skills import BasicSkills
      self._basic_skills = BasicSkills()
    return self._basic_skills
  
  def _get_automation_skills(self):
    if self._automation_skills is None:
      from friday_core.skills.automation_skills import automation_skills
      self._automation_skills = automation_skills
    return self._automation_skills
  
  def can_handle(self, command: str) -> bool:
    browser_keywords = [
      'открой', 'запусти', 'браузер', 'интернет', 'найди', 'поиск',
      'закрой', 'приложение', 'программа', 'хром', 'firefox', 'edge'
    ]
    command_lower = command.lower()
    return any(keyword in command_lower for keyword in browser_keywords)
  
  def process(self, command: str) -> str:
    command_lower = command.lower()
    basic_skills = self._get_basic_skills()
    automation_skills = self._get_automation_skills()

    if any(word in command_lower for word in ['открой браузер', 'запусти браузер', 'интернет']):
        from friday_core.config.config import config
        browser = config.get('media.browser', 'default')
        return basic_skills.open_browser(browser)
    
    elif 'открой хром' in command_lower or 'запусти хром' in command_lower:
        return basic_skills.open_browser('chrome')
    
    elif 'открой файрфокс' in command_lower or 'запусти файрфокс' in command_lower:
        return basic_skills.open_browser('firefox')
    
    elif 'открой edge' in command_lower or 'запусти edge' in command_lower:
        return basic_skills.open_browser('edge')
    
    # Поиск в интернете
    elif "найди" in command_lower or "поиск" in command_lower:
        query = command_lower.replace("найди", "").replace("поиск", "").strip()
        if query:
            return basic_skills.search_web(query)
        else:
            return "Что именно найти?"
    
    # Открытие приложений
    elif any(word in command_lower for word in ['открой', 'запусти']):
        for trigger in ['открой', 'запусти']:
            if trigger in command_lower:
                app_name = command_lower.split(trigger)[-1].strip()
                if app_name:
                    return automation_skills.open_application(app_name)
    
    # Закрытие приложений
    elif 'закрой приложение' in command_lower:
        app_name = command_lower.replace('закрой приложение', '').strip()
        return automation_skills.close_application(app_name)
    
    return "Браузерная команда не распознана"