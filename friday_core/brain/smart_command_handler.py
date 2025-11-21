# smart_command_handler.py

from friday_core.brain.intent_classifier import intent_classifier
from friday_core.brain.command_handler import CommandHandler
import time
import json
from friday_core.config.config import config
from friday_core.utills.recomendation_system import recomendation_system
import os
from friday_core.brain.ml_maintenance import MLMaintenance
from friday_core.utills.event_bus import event_bus, EventType
from friday_core.neurons.neuron_orchestrator import NeuronOrchestrator


class SmartCommandHandler(CommandHandler):
  def __init__(self):
    super().__init__()
    self.conversation_context = {}
    self.learning_enabled = True
    self.recomendation_system = recomendation_system

    self.neuron_orchestrator = NeuronOrchestrator()
    
    self._setup_event_handlers()
    self.ml_maintenance = MLMaintenance(intent_classifier)

    if not intent_classifier.is_trained:
      print('Обучаю Ml модель')
      intent_classifier.train()

  def _setup_event_handlers(self):
    # Подписка на события (можно добавить позже)
    pass

  def handle_command(self, command):
    if not command:
      return 'Не услышала вас, сэр'
    
    # пробуем через нейрон
    neuron_response = self.neuron_orchestrator.process_command(command)
    if neuron_response is not None:
      print(f'Обработано нейроном: {neuron_response}')
      return neuron_response
    
    # резерв, старая логика
    intent = intent_classifier.predict_intent(command)
    print(f'ML определил намерения: {intent}')

    event_bus.publish(EventType.COMMAND_RECEIVED, {
      'command': command,
      'timestamp': time.time()
    })

    event_bus.publish(EventType.INTENT_CLASSIFIED, {
      'command': command,
      'intent': intent,
      'confidence': 'N/A'
    })

    self._update_context(command, intent)

    if intent == 'unknown':
      response = super().handle_command(command)
    else:
      response = self._handle_by_intent(command, intent)

    event_bus.publish(EventType.COMMAND_EXECUTED, {
      'command': command,
      'intent': intent,
      'response': response,
      'success': 'ошибка' not in response.lower()
    })

    if self.learning_enabled:
      self._learn_from_interaction(command, intent, response)

    self.ml_maintenance.record_command()

    return response 
  
  def _update_context(self, command, intent):
    self.conversation_context['last_command'] = command
    self.conversation_context['last_intent'] = intent
    self.conversation_context['timestamp'] = time.time()

    if 'погода' in command.lower():
      cities = ['москв', 'рязан', 'спб', 'питер', 'казан', 'сочи']

      for city in cities:
        if city in command.lower():
          self.conversation_context['location'] = city
          break

  def _handle_by_intent(self, command, intent):

    intent_handlers = {
      'weather': self._handle_weather_intent,
      'music': self._handle_music_intent,
      'system': self._handle_system_intent,
      'browser': self._handle_browser_intent,
      'reminder': self._handle_reminder_intent,
      'screenshot': self._handle_screenshot_intent,
      'volume': self._handle_volume_intent,
      'time': self._handle_time_intent,
      'greeting': self._handle_greeting_intent,
      'farewell': self._handle_farewell_intent,
      'calendar': self._handle_calendar_intent,
      'telegram': self._handle_telegram_intent,
      'system_info': self._handle_system_info_intent,
      'application': self._handle_application_intent,
      'config': self._handle_config_intent,
      'help': self._handle_help_intent
    }

    handler = intent_handlers.get(intent, super().handle_command)
    return handler(command)
  
  def _handle_weather_intent(self, command):
    location = self.conservation_context.get('location', None)
    command_lower = command.lower()

    if 'москв' in location:
      return self.weather_skills.get_weather('Москва')
    elif 'рязан' in location:
      return self.weather_skills.get_weather('Рязань')
    elif 'спб' in location:
      return self.weather_skills.get_weather('Санкт_Петербург')
    elif 'в казани' in command_lower or 'казань' in command_lower:
      return self.weather_skills.get_weather("Казань")
    elif 'в нижегород' in command_lower or 'нижний новгород' in command_lower:
      return self.weather_skills.get_weather("Нижний Новгород")
    elif 'воронеж' in command_lower:
      return self.weather_skills.get_weather("Воронеж")
    elif 'сочи' in command_lower:
      return self.weather_skills.get_weather("Сочи")
    elif 'екб' in command_lower or 'екатеринбург' in command_lower:
      return self.weather_skills.get_weather("Екатеринбург")
    elif 'новосибирск' in command_lower:
      return self.weather_skills.get_weather("Novosibirsk")
    elif 'краснодар' in command_lower:
      return self.weather_skills.get_weather("Krasnodar")
    
    return self.weather_skills.get_weather_by_location()
  
  def _handle_music_intent(self, command):
    if 'hitmo' in command.lower() or 'hit' in command.lower():
      return self.media_skills.play_hitmo()
    
    elif 'ютуб' in command.lower() or 'youtube' in command.lower():
      if 'включи ютуб' in command.lower():
        query = command.lower().replace('включи ютуб', '').strip()
        if query:
          return self.media_skills.play_on_youtube(query)
      return self.media_skills.play_on_youtube('тренды')
    else:
      return self.media_skills.play_hitmo()
    

  def _handle_system_intent(self, command):
    if 'выключи' in command.lower():
      return super().handle_command('выключи компьютер')
    elif 'перезагрузи' in command.lower():
      return super().handle_command('перезагрузи компьютер')
    else:
      return super().handle_command(command)
    
  def _handle_browser_intent(self, command):
    if 'закрой' in command.lower():
      return super().handle_command('закрой браузер')
    else:
      search_triggers = ['найди', 'поиск', 'ищи']
      for trigger in search_triggers:
        if trigger in command.lower():
          query = command.lower().split(trigger)[-1].strip()
          if query:
            return self.basic_skills.search_web(query)
          
      return super().handle_command('открой браузер')
    
  def _learn_from_interaction(self, command, intent, response):
    try:
      log_entry = {
        'command': command,
        'intent': intent,
        'response': response[:100],
        'timestamp': time.time(),
        'success': 'ошибка' not in response.lower()
      }

      os.makedirs("ml_models", exist_ok=True)

      with open("ml_models/interaction_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    except Exception as e:
      print(f'Ошибка логирования: {e}')

  def retrain_model(self):
    print('переобучение модели на основании новвых данных....')
    return intent_classifier.train()
  
  def _handle_reminder_intent(self, command):
    command_lower = command.lower()

    if 'через' in command_lower:
      parts = command_lower.split('через')
      if len(parts) == 2:
        text_part = parts[0].strip()
        time_part = parts[1].strip()

        import re
        minutes_math = re.search(r'(\d+)\s*минут', time_part)
        if minutes_math:
          minutes = int(minutes_math.group(1))

          clean_text = text_part.replace('напомни', '').replace('напомнить', '').strip()
          if clean_text:
            return self.reminder_skills.set_reminder(clean_text, minutes)
          
    elif 'таймер' in command_lower:
      time_match = re.search(r'таймер\s+на\s+(\d+)\s*минут', command_lower)
      if time_match:
        minutes = int(time_match.group(1))
        return self.reminder_skills.set_timer(minutes)
      
    return "Скажите: 'напомни позвонить маме через 10 минут' или 'поставь таймер на 5 минут'"
  
  def _handle_screenshot_intent(self, command):
    command_lower = command.lower()

    if 'област' in command_lower or 'выдел' in command_lower:
      return self.automation_skills.take_screenshot(area=True)
    
    elif 'несколько' in command_lower or 'серии' in command_lower:
      count = 3
      numbers_map = {
        'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
        'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10
      }

      for word, num in numbers_map.items():
        if word in command_lower:
          count = num
          break

      else:
        import re
        numbers = re.findall(r'\d+', command_lower)
        if numbers:
          count = int(numbers[0])

      return self.automation_skills.take_multiple_screenshots(count=count)
    
    elif 'покажи' in command_lower or 'открой' in command_lower:
      if 'папка' in command_lower:
        return self.automation_skills.open_screenshots_folder()
      else:
        import re
        numbers = re.findall(r'\d+', command_lower)
        count = int(numbers[0]) if numbers else 5
        return self.automation_skills.list_recent_screenshots(count=count)
      
    elif 'статистика' in command_lower:
      return self.automation_skills.get_screenshots_stats()
    
    else:
      description = ''
      if 'название' in command_lower or 'назови' in command_lower:
        if 'с названием' in command_lower:
          description = command_lower.split('с названием')[-1].strip()
        elif 'назови' in command_lower:
          description = command_lower.split('назови')[-1].strip()

      return self.automation_skills.take_screenshot(description=description)
    
  def _handle_volume_intent(self, command):
    command_lower = command.lower()

    if 'максимум' in command_lower or 'полная' in command_lower:
      return self.audio_skills.set_volume(100)
        
    elif 'тише' in command_lower:
      return self.audio_skills.volume_down()
        
    elif 'громче' in command_lower:
      return self.audio_skills.volume_up()
        
    elif 'выключи звук' in command_lower or 'без звука' in command_lower:
      return self.audio_skills.mute()
        
    elif 'включи звук' in command_lower:
      return self.audio_skills.set_volume(50)
    
    elif 'на' in command_lower:
      import re
      numbers = re.findall(r'\d+', command)
      if numbers:
        level = max(0, min(100, int(numbers[0])))
        return self.audio_skills.set_volume(level)
      
    return "Скажите 'громче', 'тише', 'громкость на 50' или 'выключи звук'"
  
  def _handle_time_intent(self, command):
    command_lower = command.lower()

    if 'время' in command_lower or 'час' in command_lower:
      return self.basic_skills.get_time()
    
    elif 'дата' in command_lower or 'число' in command_lower or 'сегодня' in command_lower:
      return self.basic_skills.get_date()
        
    elif 'сколько времени' in command_lower or 'который час' in command_lower:
      return self.basic_skills.get_time()
        
    return "Скажите 'время' или 'дата'"
  
  def _handle_greeting_intent(self, command):
    from friday_core.config.personalization import personalization
    return personalization.get_personalized_greeting()
  
  def _handle_farewell_intent(self, command):
    from brain.intent_classifier import intent_classifier
    farewell_responses = [
      "До свидания, сэр! Жду вашего возвращения.",
      "Всего хорошего! Буду ждать следующих команд.",
      "Пока! Не скучайте без меня.",
      "До встречи! Если что - я всегда здесь.",
      "Завершаю работу. Возвращайтесь скорее!"
    ]
        
    import random
    response = random.choice(farewell_responses)
        
        # Сохраняем контекст для корректного выхода
    self.conservation_context['should_exit'] = True
        
    return response
  
  def _handle_calendar_intent(self, command):
    from skills.calendar_skills import calendar_skills
    command_lower = command.lower()

    if 'добавь' in command_lower or 'новое событие':
      self._handle_calendar_add(command)

    elif 'удали событие' in command_lower:
      import re
      numbers = re.findall(r'\d+', command)

      if numbers:
        return calendar_skills.delete_event(numbers[0])
      else:
        return "Укажите ID события: 'удали событие 1'"
      
    elif 'сегодня' in command_lower:
      return calendar_skills.get_today_events()
    
    else:
      return calendar_skills.get_events()
    
  def _handle_system_info_intent(self,command):
    command_lower = command.lower()

    if 'систем' in command_lower or 'ресурс' in command_lower:
      return self.system_info.get_info()
    
    elif 'батарея' in command_lower or 'заряд' in command_lower:
      return self.automation_skills.get_battery_status()
    elif 'процесс' in command_lower or 'груз' in command_lower:
      return self.automation_skills.list_running_processes()
    
    return self.system_info.get_info()
  
  def _handle_application_intent(self, command):
    command_lower = command.lower()

    app_keywords = {
      'word': 'word', 'ворд': 'word', 'winword': 'word',
      'excel': 'excel', 'эксель': 'excel',
      'powerpoint': 'powerpoint', 'пауэрпоинт': 'powerpoint', 'powerpnt': 'powerpoint',
      'outlook': 'outlook', 'аутлук': 'outlook',
        
        # Системные приложения
      'блокнот': 'notepad', 'notepad': 'notepad',
      'калькулятор': 'calc', 'calc': 'calc', 'кальк': 'calc',
      'проводник': 'explorer', 'explorer': 'explorer',
      'панель управления': 'control', 'control': 'control',
      'диспетчер задач': 'taskmgr', 'taskmgr': 'taskmgr',
      'пайнт': 'mspaint', 'краска': 'mspaint', 'paint': 'mspaint',
        
        # Браузеры
      'хром': 'chrome', 'chrome': 'chrome',
      'файрфокс': 'firefox', 'firefox': 'firefox',
      'edge': 'edge', 'эдж': 'edge', 'msedge': 'edge',
      'опера': 'opera', 'opera': 'opera',
      'яндекс': 'yandex', 'yandex': 'yandex',
        
        # Мессенджеры
      'телеграм': 'telegram', 'telegram': 'telegram',
      'дискорд': 'discord', 'discord': 'discord',
      'ватсап': 'whatsapp', 'whatsapp': 'whatsapp',
      'скайп': 'skype', 'skype': 'skype',
        
        # Другое
      'вк': 'vk', 'vk': 'vk',
      'видеоплеер': 'wmplayer', 'плеер': 'wmplayer',
      'камера': 'camera', 'camera': 'camera'
    }

    if 'закрой' in command_lower or 'заверши' in command_lower:

      clean_command = command_lower.replace('закрой', '').replace('заверши', '').strip()
      for keyword, app_name in app_keywords.items():
        if keyword in clean_command:
          return self.automation_skills.close_application(app_name)
      return 'Какое приложение закрыть?'
    
    else:
      for keyword, app_name in app_keywords.items():
        if keyword in command_lower:
          return self.automation_skills.open_application(app_name)
        
      open_triggers = ['открой', 'запусти', 'включи']
      for trigger in open_triggers:
        if trigger in command_lower:
          app_name = command_lower.split(trigger)[-1].strip()
          if app_name:
            return self.automation_skills.open_application(app_name)
      return 'Какое приложение запустить?'
    
  def _handle_config_intent(self, command):
    command_lower = command.lower()

    if 'очисти логи' in command_lower or 'почисти логи' in command_lower:
      return self.ml_maintenance.manual_cleanup()
    
    elif 'переобучи модель' in command_lower or 'обнови модель' in command_lower:
      return self.ml_maintenance.manual_retrain()
    
    elif 'статус модели' in command_lower or 'состояние модели' in command_lower:
      status = self.ml_maintenance.get_status()
      return (f"📊 Статус ML модели:\n"
              f"Команд с последнего обучения: {status['commands_since_training']}\n"
              f"До следующего обучения: {status['commands_until_retrain']} команд\n"
              f"Максимум логов: {status['max_logs']}\n"
              f"Максимум последовательностей: {status['max_sequences']}")
      

    if 'настройки' in command_lower or 'конфиг' in command_lower:
      return self._show_config()
    
    elif 'сброс' in command_lower:
      return config.reset_to_defaults()
    
    elif 'город' in command_lower:
      if 'измени город' in command_lower or 'смени город' in command_lower:
        city = command_lower.replace('измени город', '').replace('смени город','').strip()
        if city:
          config.set('location.default_city', city)
          return f'город по умолчанию изменен на {city}'
        
    elif 'голос' in command_lower:
      if 'смени голос' in command_lower:
        voices_map = {
          'светлана': 'ru-RU-SvetlanaNeural',
          'дмитрий': 'ru-RU-DmitryNeural', 
          'никита': 'ru-RU-NikitaNeural',
          'дария': 'ru-RU-DariyaNeural'
        }

        for key, voice_id in voices_map.items():
          if key in command_lower:
            if hasattr(self.voice_engine, 'tts_engine'):
              self.voice_engine.tts_engine.set_voice(voice_id)
              return f'Голос изменен на {key}'
            
        return 'Доступные голоса: светлана, дмитрий, никита, дария'
      
    return self._show_config()
  
  def _handle_help_intent(self, command):
    last_intent = self.conversation_context.get('last_intent')
        
    if last_intent:
            # Контекстная помощь
      context_help = {
        'weather': "Вы можете спросить: 'погода', 'погода в Москве', 'температура'",
        'music': "Команды: 'включи музыку', 'включи ютуб', 'пауза'",
        'system': "Управление системой: 'выключи компьютер', 'перезагрузи', 'отмени выключение'",
        'screenshot': "Скриншоты: 'сделай скриншот', 'скриншот области', 'покажи скриншоты'",
        'reminder': "Напоминания: 'напомни позвонить через 10 минут', 'поставь таймер на 5 минут'",
        'telegram': "Telegram: 'настрой телеграм', 'отправь сообщение', 'статус телеграм'"
      }

      if last_intent in context_help:
        return f'Помощь по {last_intent}: \n{context_help[last_intent]}'
      
    return self._get_help_message()
  
  def get_smart_recommendations(self):
    
    base_recs = self.recomendation_system.get_recomendations(2)

    last_intent = self.conversation_context.get('last_intent')
    context_recs = []

    if last_intent == 'weather':
      context_recs = ["Узнать погоду в другом городе", "Посмотреть прогноз на завтра"]
    elif last_intent == 'music':
      context_recs = ["Включить другой плейлист", "Поставить на паузу"]
    elif last_intent == 'screenshot':
      context_recs = ["Открыть папку скриншотов", "Сделать скриншот области"]

    return base_recs + context_recs[:1]
  
  def _handle_telegram_intent(self, command):
    command_lower = command.lower()

    if any(word in command_lower for word in ['настрой telegram', 'настройка telegram']):
      return self._handle_telegram_setup(command)
    elif any(word in command_lower for word in['получи id', 'id telegram']):
      return self._handle_telegram_get_id(command)
    elif any(word in command_lower for word in ['отправь в telegram', 'сообщение в telegram']):
      return self._handle_telegram_send_message(command)
    elif any(word in command_lower for word in ['статус telegram', 'telegram статус']):
      return self._handle_telegram_status(command)
    else:
      return "Команды Telegram: 'настрой телеграм', 'отправь сообщение', 'статус телеграм'"
    
  def _handle_telegram_setup(self, command):
    from skills.telegram_skills import telegram_skills
    return telegram_skills.setup_bot()
  
  def _handle_telegram_get_id(self, command):
    from skills.telegram_skills import telegram_skills
    return telegram_skills.get_updates()
  
  def _handle_telegram_send_message(self, command):
    from skills.telegram_skills import telegram_skills
    if 'отправь в телеграм' in command.lower():
      text = command.split('отправь в телеграм')[-1].strip()

    elif 'отправь в telegram' in command.lower():
      text = command.split('отправь в telegram')[-1].strip()
    else:
      text = command.split('сообщение в telegram')[-1].strip()

    if text:
      return telegram_skills.send_message(text)
    else:
      return 'Укажите текст сообщения'
    
  def _handle_telegram_status(self, command):
    from skills.telegram_skills import telegram_skills
    return telegram_skills.get_status()
  
  