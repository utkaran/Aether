# command_handler.py

from friday_core.skills.basic_skills import BasicSkills
from friday_core.skills.system_skills import SystemSkills
from friday_core.skills.media_skills import MediaKills
from friday_core.skills.reminder_skills import ReminderSkills
from friday_core.skills.audio_skills import AudioSkills
from friday_core.skills.working_system_info import WorkingSystemInfo
from friday_core.skills.weather_skills import WeatherSkills
from friday_core.config.config import config
from friday_core.skills.calendar_skills import calendar_skills
from friday_core.engine.voice_engine import VoiceEngine
from friday_core.skills.automation_skills import automation_skills
from friday_core.skills.telegram_skills import telegram_skills
from friday_core.config.personalization import personalization
from phone_bridge import phone_bridge
from friday_core.neurons.neuron_orchestrator import NeuronOrchestrator



class CommandHandler:
    def __init__(self):
        self.basic_skills = BasicSkills()
        self.system_skills = SystemSkills()
        self.weather_skills = WeatherSkills()
        self.voice_engine = VoiceEngine()


        self.media_skills = None
        self.reminder_skills = None
        self.audio_skills = None
        self.system_info = None
        self.automation_skills = None
        self.phone_bridge = None

        self.neuron_orchestrator = NeuronOrchestrator()

    def get_media_skills(self):
        """Безопасная ленивая загрузка media_skills"""
        if self._media_skills is None:
            from friday_core.skills.media_skills import MediaKills
            self._media_skills = MediaKills()
        return self._media_skills
    
    def get_reminder_skills(self):
        """Безопасная ленивая загрузка reminder_skills"""
        if self._reminder_skills is None:
            from friday_core.skills.reminder_skills import ReminderSkills
            self._reminder_skills = ReminderSkills()
        return self._reminder_skills
    
    def get_audio_skills(self):
        """Безопасная ленивая загрузка audio_skills"""
        if self._audio_skills is None:
            from friday_core.skills.audio_skills import AudioSkills
            self._audio_skills = AudioSkills()
        return self._audio_skills
    
    def get_system_info(self):
        """Безопасная ленивая загрузка system_info"""
        if self._system_info is None:
            from friday_core.skills.working_system_info import WorkingSystemInfo
            self._system_info = WorkingSystemInfo()
        return self._system_info
    
    def get_automation_skills(self):
        """Безопасная ленивая загрузка automation_skills"""
        if self._automation_skills is None:
            from friday_core.skills.automation_skills import automation_skills
            self._automation_skills = automation_skills
        return self._automation_skills
    
    def get_phone_bridge(self):
        """Безопасная ленивая загрузка phone_bridge"""
        if self._phone_bridge is None:
            from phone_bridge import phone_bridge
            self._phone_bridge = phone_bridge
        return self._phone_bridge
    
    def handle_command(self, command):
        """Основной обработчик команд"""
        if not command:
            return "Не услышал вас, сэр, повторите пожалуйста"
        
        command_lower = command.lower()


        print(f"🔍 Команда в нижнем регистре: '{command_lower}'")

        personalization.update_usage_statistics(command)

        if any(word in command_lower for word in['привет', "здравствуй", "добрый", "хай"]):
            return personalization.get_personalized_greeting()
        
        elif 'нейроны' in command_lower:
            if 'статус' in command_lower:
                status = self.neuron_orchestrator.get_status()
                response = f'Статус нейронов: {status["active"]}/{status["total"]} активны'
                for name, details in status['details'].items():
                    status_icon = "🟢" if details['active'] else "🔴"
                    response += f'{status_icon} {name} (ошибок: {details["errors"]})\n'
                return response
            
            elif 'перезапусти' in command_lower:
                return self.neuron_orchestrator.restart_all_neurons()
            
            elif 'список' in command_lower:
                status = self.neuron_orchestrator.get_status()
                neuron_list = "\n".join([f"- {name}" for name in status['details'].keys()])
                return f'Список нейронов:\n{neuron_list}'
            
        if any(word in command_lower for word in ['статус системы', 'здоровье системы', 'мониторинг']):
            status = self.get_system_status()
            return (f"📊 Статус системы:\n"
                    f"CPU: {status['health']['current_cpu']:.1f}%\n"
                    f"Память: {status['health']['current_memory']:.1f}%\n"
                    f"Команд обработано: {status['performance']['total_commands']}\n"
                    f"Среднее время: {status['performance']['avg_processing_time']:.2f}с\n"
                    f"Активных нейронов: {status['neurons']['active']}/{status['neurons']['total']}")
        
        elif 'очисти кэш' in command_lower:
            if hasattr(self, '_response_cache'):
                with self._cache_lock:
                    self._response_cache.clear()
                self._preprocess_command.cache_clear()
                return "✅ Кэш очищен"
        
        if 'зовут' in command_lower and 'меня' in command_lower:
            name = command_lower.split('меня')[-1].replace('зовут', '').strip()
            if name:
                return personalization.set_user_name(name)
            
        elif 'измени' in command_lower:
            if 'профессиональный' in command_lower:
                return personalization.set_response_style('professional')
            elif 'дружелюбный' in command_lower:
                return personalization.set_response_style('friendly')
            elif 'неформальный' in command_lower:
                return personalization.set_response_style('casual')
            else:
                return 'Доступные стили: профессиональный, дружелюбный, неформальный'
            
        elif 'любимый город' in command_lower:
            if 'добавь' in command_lower:
                city = command_lower.lower().split('добавь')[-1].replace('любимый город', '').strip()
                return personalization.add_favorite_city(city)
            else:
                return f'Ваш любимый город : {personalization.get_favorite_city()}'
            
        elif "моя статистика" in command.lower() or "частые команды" in command.lower():
            frequent_commands = personalization.get_frequent_commands(5)
            result = "Ваши частые команды:\n"
            for i, (cmd, count) in enumerate(frequent_commands, 1):
                result += f"{i}. {cmd} - {count} раз\n"
            return result
        
        elif 'персональная помощь' in command_lower:
            return personalization.get_personalized_help()
        
        elif 'предложения' in command_lower:
            suggestions = personalization.get_time_based_suggestions()
            result = 'Сейчас вам могут быть полезны:\n'
            for i, suggestion in enumerate(suggestions, 1):
                result += f'{i}. {suggestion}\n'
            return result

        if any(word in command_lower for word in ["скриншот", "снимок", "скрин"]):
            print("🎯 Обрабатываю команду скриншота...")
            
            # Сначала проверяем команды ПРОСМОТРА и УПРАВЛЕНИЯ скриншотами
            if any(word in command_lower for word in ["покажи", "показать", "открой", "открыть", "последние"]):
                if "папк" in command_lower:
                    return self.get_automation_skills.open_screenshots_folder()
                else:
                    import re
                    numbers = re.findall(r'\d+', command_lower)
                    count = int(numbers[0]) if numbers else 5
                    return self.get_automation_skills.list_recent_screenshots(count=count)
            
            elif any(word in command_lower for word in ["статистика", "сколько", "статус"]):
                return self.get_automation_skills.get_screenshots_stats()
            
            elif any(word in command_lower for word in ["удали", "очистки", "удалить", "очистить"]):
                import re
                numbers = re.findall(r'\d+', command_lower)
                days = int(numbers[0]) if numbers else 30
                return self.get_automation_skills.cleanup_old_screenshots(days=days)

        if any(word in command_lower for word in ["сделай", "сними", "создай"]):
            print("🎯 Обрабатываю команду скриншота...")
            
            # Обработка числительных
            numbers_map = {
                'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
                'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10
            }
            
            # Определяем количество скриншотов
            count = 1
            for word, num in numbers_map.items():
                if word in command_lower:
                    count = num
                    break
            else:
                # Ищем цифры
                import re
                numbers = re.findall(r'\d+', command_lower)
                if numbers:
                    count = int(numbers[0])
            
            # Определяем тип скриншота
            if "области" in command_lower or "выдели" in command_lower:
                return self.get_automation_skills.take_screenshot(area=True)
            elif count > 1:
                return self.get_automation_skills.take_multiple_screenshots(count=count)
            else:
                # Извлекаем описание если есть
                description = ""
                if "с названием" in command_lower:
                    description = command_lower.split("с названием")[-1].strip()
                elif "назови" in command_lower:
                    description = command_lower.split("назови")[-1].strip()
                return self.get_automation_skills.take_screenshot(description=description)

        

        # Сначала проверяем команды конфигурации
        config_response = self.handle_config_command(command)
        if config_response:
            return config_response
        
        if "доступные голоса" in command_lower or "покажи голоса" in command_lower:
            return self._handle_voice_list()
    
        if "смени голос" in command_lower:
            return self._handle_voice_change(command_lower)
        
        # УДАЛЕНО: рекурсивный вызов handle_config_command
        
        if "добавь событие" in command_lower or "новое событие" in command_lower:
            return self._handle_calendar_add(command)
        
        elif "календарь" in command_lower or "события" in command_lower:
            if "сегодня" in command_lower:
                return calendar_skills.get_today_events()
            else:
                return calendar_skills.get_events()
            
        elif "удали событие" in command_lower:
            import re
            numbers = re.findall(r'\d+', command)
            if numbers:
                return calendar_skills.delete_event(numbers[0])
            else:
                return "Укажите ID события: удали событие 1"

        # Обработка системных команд
        if command_lower == 'отмени выключение':
            print('Отмена выключения...')
            return self.system_skills.cancel_shutdown()
        
        elif "перезагрузи" in command_lower or "перезагрузка" in command_lower:
            print("🔍 ОТЛАДКА: Обнаружено слово 'перезагрузи'")
    
            import re
            numbers = re.findall(r'\d+', command)
            seconds = config.get('system.shutdown_timeout', 15)
    
            if numbers:
                seconds = int(numbers[0])
                print(f"🔍 ОТЛАДКА: Найдено время: {seconds} секунд")
    
            print(f"✅ Перезагрузка через {seconds} секунд!")
            return self.system_skills.restart(seconds)
                
        elif "выключи" in command_lower:
            print("🔍 ОТЛАДКА: Обнаружено слово 'выключи'")
    
            # Ищем время в команде
            import re
            numbers = re.findall(r'\d+', command)
            seconds = config.get('system.shutdown_timeout', 15)  # значение из конфига
    
            if numbers:
                seconds = int(numbers[0])
                print(f"🔍 ОТЛАДКА: Найдено время: {seconds} секунд")
    
            # Проверяем разные варианты команды
            if "компьютер" in command_lower or "пк" in command_lower:
                print(f"✅ Выключение через {seconds} секунд!")
                return self.system_skills.shutdown(seconds)
            else:
                # Если просто "выключи" без уточнения
                return "Уточните: выключи компьютер или выключи через 10 секунд"

        # Управление громкостью (ОДИН блок - удалены дубликаты)
        if "громкость на" in command_lower:
            # Пример: "громкость на 50"
            import re
            numbers = re.findall(r'\d+', command)
            if numbers:
                level = int(numbers[0])
                return self.get_audio_skills.set_volume(level)
            else:
                return "Укажите уровень: громкость на 50"
        
        elif "громкость максимум" in command_lower or "полная громкость" in command_lower:
            return self.get_audio_skills.set_volume(100)
        
        elif "тише" in command_lower:
            return self.get_audio_skills.volume_down()
        
        elif "громче" in command_lower:
            return self.get_audio_skills.volume_up()
        
        elif "выключи звук" in command_lower or "без звука" in command_lower:
            return self.get_audio_skills.mute()
        
        elif "включи звук" in command_lower:
            return self.get_audio_skills.set_volume(50)
        
        elif command_lower == "громкость":
            # Если просто сказали "громкость" - показываем текущий статус
            return "Скажите 'громче', 'тише', 'громкость на 50' или 'выключи звук'"
        
        elif any(word in command_lower for word in['открой', 'запусти']):
            for trigger in ['открой', 'запусти']:
                if trigger in command_lower:
                    app_name = command_lower.split(trigger)[-1].strip()
                    return self.get_automation_skills.open_application(app_name)
                
        elif 'закрой приложение' in command_lower:
            app_name = command_lower.replace('закрой приложение', '').strip()
            return self.get_automation_skills.close_application(app_name)
        
        elif "сделай скриншот" in command_lower:
            if "области" in command_lower:
                return self.get_automation_skills.take_screenshot(area=True)
            elif "несколько" in command_lower or "серию" in command_lower or any(word in command_lower for word in ["два", "три", "четыре", "пять"]):
                # Обработка числительных
                numbers_map = {
                    'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
                    'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10
                }
                
                # Ищем числительные в команде
                count = 3  # значение по умолчанию
                for word, num in numbers_map.items():
                    if word in command_lower:
                        count = num
                        break
                else:
                    # Если числительных нет, ищем цифры
                    import re
                    numbers = re.findall(r'\d+', command_lower)
                    if numbers:
                        count = int(numbers[0])
                
                return self.get_automation_skills.take_multiple_screenshots(count=count)
            else:
                # Извлекаем описание если есть
                description = ""
                if "с названием" in command_lower:
                    description = command_lower.split("с названием")[-1].strip()
                return self.get_automation_skills.take_screenshot(description=description)

        elif "покажи скриншоты" in command_lower or "последние скриншоты" in command_lower:
            import re
            numbers = re.findall(r'\d+', command_lower)
            count = int(numbers[0]) if numbers else 5
            return self.get_automation_skills.list_recent_screenshots(count=count)

        elif "открой папку скриншотов" in command_lower or "папка скриншотов" in command_lower:
            return self.get_automation_skills.open_screenshots_folder()

        elif "статистика скриншотов" in command_lower or "сколько скриншотов" in command_lower:
            return self.get_automation_skills.get_screenshots_stats()

        elif "очисти старые скриншоты" in command_lower:
            import re
            numbers = re.findall(r'\d+', command_lower)
            days = int(numbers[0]) if numbers else 30
            return self.get_automation_skills.cleanup_old_screenshots(days=days)
            
        elif any(word in command_lower for word in['ресурсы системы', 'загрузка системы', 'системные ресурсы']):
            return self.get_automation_skills.get_system_resources()
        
        elif any(word in command_lower for word in['сверни все', 'рабочий стол', 'переключи окно', 'закрой окно']):
            action = command_lower
            return self.get_automation_skills.window_management(action)
        
        elif 'введи текст' in command_lower:
            text = command_lower.replace('введи текст', '').strip()
            return self.get_automation_skills.type_text(text)
        
        elif 'нажми' in command_lower:
            key = command_lower.replace('нажми', '').strip()
            return self.get_automation_skills.press_key(key)
        
        elif 'батарея' in command_lower or 'заряд' in command_lower:
            return self.get_automation_skills.get_battery_status()
        
        elif 'процессы' in command_lower or 'что грузит' in command_lower:
            return self.get_automation_skills.list_running_processes()
        
        elif 'очисти систему' in command_lower or 'очистка системы' in command_lower:
            return self.get_automation_skills.system_cleanup()
                
        if any(word in command_lower for word in ["информация о системе", "системная информация", "информация система", "система"]):
            print("✅ Распознана команда 'информация о системе'")
            return self.get_system_info.get_info()
        
        elif 'Выключи компьютер' in command_lower:
            import re
            numbers = re.findall(r'\d+', command)
            if numbers and int(numbers[0]) > 0:
                seconds = int(numbers[0])
                return self.system_skills.shutdown(seconds)
            else:
                # По умолчанию из конфига
                seconds = config.get('system.shutdown_timeout', 15)
                return self.system_skills.shutdown(seconds)
        
        elif "перезагрузи компьютер" in command_lower:
            import re
            numbers = re.findall(r'\d+', command)
            if numbers and int(numbers[0]) > 0:
                seconds = int(numbers[0])
                return self.system_skills.restart(seconds)
            else:
                seconds = config.get('system.shutdown_timeout', 15)
                return self.system_skills.restart(seconds)
            
        # Медиа команды
        elif 'включи музыку' in command:
            return self.get_media_skills.play_hitmo()
        elif 'hitmo' in command_lower:
            return self.get_media_skills.play_hitmo()
        elif 'включи youtube' in command:
            return self.get_media_skills.play_on_youtube('тренды')
        elif 'пауза' in command:
            return self.get_media_skills.pause_media()
        
        # Напоминания и таймеры
        elif 'напомни' in command:
            parts = command.split('напомни')[1].split('через')
            if len(parts) == 2:
                text = parts[0].strip()
                minutes = int(parts[1].split()[0])
                return self.reminder_skills.set_reminder(text, minutes)
            return 'Формат, что [что] через [сколько] минут'
        
        elif 'какие напоминания' in command:
            return self.get_reminder_skills.get_reminders()
        
        elif "поставь таймер" in command:
            # Пример: "поставь таймер на 5 минут"
            parts = command.split("таймер на")
            if len(parts) == 2:
                minutes = int(parts[1].split()[0])
                return self.get_reminder_skills.set_timer(minutes)
            return "Формат: поставь таймер на [сколько] минут"
        
        # 🌤️ КОМАНДЫ ПОГОДЫ
        elif "погода" in command_lower:
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
            
        # Приветствия
        if any(word in command for word in ["привет", "здравствуй", "добрый день", "хай"]):
            return "Здравствуйте! Чем могу помочь?"
        
        # Время
        elif any(word in command for word in ["время", "час", "времени", "который час"]):
            return self.basic_skills.get_time()
        
        # Дата
        elif any(word in command for word in ["дата", "число", "какое число", "сегодня"]):
            return self.basic_skills.get_date()
        
        elif any(word in command for word in ["открой браузер", "запусти браузер", "интернет"]):
            browser = config.get('media.browser', 'default')
            return self.basic_skills.open_browser(browser)
        
        elif "открой хром" in command or "запусти хром" in command:
            return self.basic_skills.open_browser('chrome')
        
        elif "открой файрфокс" in command or "запусти файрфокс" in command:
            return self.basic_skills.open_browser('firefox')
        
        elif "открой edge" in command or "запусти edge" in command:
            return self.basic_skills.open_browser('edge')
        
        elif "открой о" in command or "запусти о" in command:
            return self.basic_skills.open_browser('opera')
        
        elif "открой яндекс" in command or "запусти яндекс" in command:
            return self.basic_skills.open_browser('Yandex')
        
        # Браузер
        elif any(word in command for word in ['закрой браузер']):
            if self.basic_skills.close_browser():
                return 'Браузер закрыт'
            else:
                return 'Браузер не найден или уже закрыт'
            
        elif "закрой хром" in command or "закрыть хром" in command:
            if self.basic_skills.close_browser('chrome'):
                return "Google Chrome закрыт"
            else:
                return "Chrome не найден"
        
        elif "закрой файрфокс" in command or "закрыть файрфокс" in command:
            if self.basic_skills.close_browser('firefox'):
                return "Firefox закрыт"
            else:
                return "Firefox не найден"
        
        elif "закрой edge" in command or "закрыть edge" in command:
            if self.basic_skills.close_browser('edge'):
                return "Microsoft Edge закрыт"
            else:
                return "Edge не найден"
            
        elif 'закрой о' in command or 'закрыть о' in command:
            if self.basic_skills.close_browser('opera'):
                return 'опера закрыта'
            else:
                return 'опера не найдена'
            
        elif 'закрой яндекс' in command or 'закрыть яндекс' in command:
            if self.basic_skills.close_browser('Yandex'):
                return 'яндекс закрыт'
            else:
                return 'яндекс не найден'
        
        # Поиск в интернете
        elif "найди" in command or "поиск" in command:
            query = command.replace("найди", "").replace("поиск", "").strip()
            if query:
                return self.basic_skills.search_web(query)
            else:
                return "Что именно найти?"
            
        if any(word in command_lower for word in ['настрой telegram', 'настрой телеграм', 'настройка телеграм']):
            return telegram_skills.setup_bot()
        
        elif any(word in command_lower for word in['получи id telegram', 'получить айди телеграм', 'получи айди телеграм', 'айди телеграм']):
            return telegram_skills.get_updates()
        
        elif any(word in command_lower for word in ['отправь в телеграм', 'сообщение в телеграм', 'отправь в telegram']):
            # Извлекаем текст сообщения
            if 'отправь в телеграм' in command_lower:
                text = command.split('отправь в телеграм')[-1].strip()
            elif 'отправь в telegram' in command_lower:
                text = command.split('отправь в telegram')[-1].strip()
            else:
                text = command.split('сообщение в телеграм')[-1].strip()
            
            if text:
                return telegram_skills.send_message(text)
            else:
                return "Укажите текст сообщения: 'отправь в телеграм привет как дела'"
            
        elif any(word in command_lower for word in ['отправь скриншот в телеграм', 'скриншот в телеграм', 'отправь скрин в телеграм']):
    # Сначала делаем скриншот, потом отправляем
            from pathlib import Path
            screenshot_result = self.automation_skills.take_screenshot()
            if 'сохранен' in screenshot_result.lower():
                # Получаем последний файл в папке скриншотов
                screenshots_dir = self.automation_skills.current_screenshots_dir
                if screenshots_dir.exists():
                    # Ищем самый новый PNG файл
                    png_files = list(screenshots_dir.glob('*.png'))
                    if png_files:
                        # Сортируем по времени изменения (новые сначала)
                        png_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                        latest_screenshot = png_files[0]
                        return telegram_skills.send_photo(str(latest_screenshot), '📸 Скриншот от Пятницы')
                return '❌ Не удалось найти скриншот для отправки'
            else:
                return screenshot_result
            
        elif any(word in command_lower for word in ['статус телеграм', 'телеграм статус', 'статус telegram']):
            return telegram_skills.get_status()

 
        # Заметки
        elif "заметка" in command or "запиши" in command:
            note_text = command.replace("заметка", "").replace("запиши", "").strip()
            if note_text:
                return self.basic_skills.create_note(note_text)
            else:
                return "Что записать в заметку?"
        
        # Помощь
        elif any(word in command for word in ["помощь", "команды", "умеешь"]):
            return self._get_help_message()
        
        # Прощание
        elif any(word in command for word in ["пока", "выход", "стоп", "заверши", 'отдыхай']):
            return "До свидания, сэр"
        
        else:
            return "Извините, я не понял команду. Скажите 'помощь' для списка команд."
    
    def handle_config_command(self, command):
    
        command_lower = command.lower()

        # Сброс настроек
        if "сбрось настройки" in command_lower or "настройки по умолчанию" in command_lower:
            return config.reset_to_defaults()
        
        elif "включи звуки" in command_lower:
            config.set('sounds.enabled', True)
            from friday_core.engine.sound_manager import sound_manager
            sound_manager.set_volume(True)
            return "Звуковые эффекты включены"

        elif "выключи звуки" in command_lower:
            config.set('sounds.enabled', False)
            from friday_core.engine.sound_manager import sound_manager
            sound_manager.set_volume(False)
            return "Звуковые эффекты выключены"
        
        # Показать настройки
        elif "покажи настройки" in command_lower or "текущие настройки" in command_lower:
            return self._show_config()
        
        # Изменить город
        elif "измени город" in command_lower or "смени город" in command_lower:
            city = command_lower.replace("измени город", "").replace("смени город", "").strip()
            if city:
                config.set('location.default_city', city)
                return f"Город по умолчанию изменен на {city}"
            else:
                return "Укажите город: измени город Москва"
        
        # Громкость речи
        elif "громкость речи" in command_lower:
            import re
            numbers = re.findall(r'\d+', command)
            if numbers:
                volume = max(0, min(100, int(numbers[0])))
                # Обновляем Edge-TTS
                if hasattr(self.voice_engine, 'tts_engine'):
                    self.voice_engine.tts_engine.set_volume(volume)
                return f"Громкость речи установлена на {volume}%"
            else:
                current_volume = config.get('voice.volume', 50)
                return f"Текущая громкость речи: {current_volume}%"
        
        # Скорость речи
        elif "скорость речи" in command_lower:
            import re
            numbers = re.findall(r'\d+', command)
            if numbers:
                speed = max(50, min(300, int(numbers[0])))
                # Обновляем Edge-TTS
                if hasattr(self.voice_engine, 'tts_engine'):
                    self.voice_engine.tts_engine.set_rate(speed)
                return f"Скорость речи установлена на {speed}"
            else:
                current_speed = config.get('voice.rate', 150)
                return f"Текущая скорость речи: {current_speed}"
        
        # Время выключения
        elif "время выключения" in command_lower or "таймаут выключения" in command_lower:
            import re
            numbers = re.findall(r'\d+', command)
            if numbers:
                timeout = max(5, min(300, int(numbers[0])))
                config.set('system.shutdown_timeout', timeout)
                return f"Время до выключения установлено на {timeout} секунд"
            else:
                current_timeout = config.get('system.shutdown_timeout', 15)
                return f"Текущее время до выключения: {current_timeout} секунд"
        
        # Сменить браузер по умолчанию
        elif "браузер по умолчанию" in command_lower:
            browsers = {
                'хром': 'chrome',
                'chrome': 'chrome',
                'файрфокс': 'firefox', 
                'firefox': 'firefox',
                'эдж': 'edge',
                'edge': 'edge',
                'опера': 'opera',
                'opera': 'opera',
                'яндекс': 'yandex',
                'yandex': 'yandex'
            }
            
            for key, value in browsers.items():
                if key in command_lower:
                    config.set('media.browser', value)
                    return f"Браузер по умолчанию изменен на {value}"
            
            return "Укажите браузер: хром, файрфокс, эдж, опера или яндекс"
        
        # Отладка голоса
        elif "отладка голоса" in command_lower:
            return self._debug_voice_settings()
        
        # Принудительная установка голоса
        elif "используй светлану" in command_lower:
            return self._force_set_voice('ru-RU-SvetlanaNeural', 'Светлана')
        
        # Текущий голос
        elif "текущий голос" in command_lower:
            return self._get_current_voice()
        
        elif 'текущий голос' in command_lower or 'какой голос' in command_lower:
            if hasattr(self.voice_engine, 'tts_engine'):
                current_voice = self.voice_engine.tts_engine.voice
                voice_names = {
                    'ru-RU-SvetlanaNeural': 'Светлана',
                    'ru-RU-DmitryNeural': 'Дмитрий', 
                    'ru-RU-NikitaNeural': 'Никита',
                    'ru-RU-DariyaNeural': 'Дария'
                }

                display_name = voice_names.get(current_voice, current_voice)
                return f"Текущий голос: {display_name}"
            return "TTS движок не доступен"
        
        # Перезагрузка TTS
        elif "перезагрузи tts" in command_lower:
            return self._reload_tts()
        
        return None
    
    def _debug_voice_settings(self):
        """Отладочная информация о голосе"""
        current_voice = config.get('voice.edge_voice', 'не установлен')
        tts_provider = config.get('voice.tts_provider', 'не установлен')
        
        debug_info = f"""
🔊 ОТЛАДКА НАСТРОЕК ГОЛОСА:
- Голос в конфиге: {current_voice}
- Провайдер TTS: {tts_provider}
"""
        
        if hasattr(self.voice_engine, 'tts_engine'):
            debug_info += f"- Используемый голос: {getattr(self.voice_engine.tts_engine, 'voice', 'не доступен')}\n"
            debug_info += f"- Используемая скорость: {getattr(self.voice_engine.tts_engine, 'rate', 'не доступна')}\n"
        
        print(debug_info)
        return debug_info
    
    def _force_set_voice(self, voice_id, voice_name):
        """Принудительная установка голоса"""
        if hasattr(self.voice_engine, 'tts_engine'):
            self.voice_engine.tts_engine.set_voice(voice_id)
            # Принудительно сохраняем в конфиг
            config.set('voice.edge_voice', voice_id)
            return f"✅ Голос принудительно установлен на {voice_name}"
        return "❌ TTS движок не доступен"
    
    def _get_current_voice(self):
        """Получить текущий голос"""
        if hasattr(self.voice_engine, 'tts_engine'):
            current_voice = getattr(self.voice_engine.tts_engine, 'voice', 'неизвестно')
            config_voice = config.get('voice.edge_voice', 'не установлен')
            return f"🎯 Текущий голос: {current_voice}\n⚙️ В конфиге: {config_voice}"
        return "❌ TTS движок не доступен"
    
    def _reload_tts(self):
        """Перезагружает TTS движок"""
        if hasattr(self.voice_engine, 'tts_engine'):
            # Получаем текущие настройки из конфига
            voice = config.get('voice.edge_voice', 'ru-RU-SvetlanaNeural')
            rate = config.get('voice.rate', 150)
            
            # Пересоздаем движок
            from friday_core.engine.ffplay_tts import FFplayTTS
            self.voice_engine.tts_engine = FFplayTTS()
            
            # Принудительно устанавливаем настройки
            self.voice_engine.tts_engine.set_voice(voice)
            self.voice_engine.tts_engine.set_rate(rate)
            
            return f"✅ TTS перезагружен. Голос: {voice}"
        return "❌ Не удалось перезагрузить TTS"
    
    def _show_config(self):
        """Показать текущие настройки"""
        current_city = config.get('location.default_city', 'Рязань')
        speech_volume = int(config.get('voice.volume', 1.0) * 100)
        speech_speed = config.get('voice.rate', 150)
        shutdown_timeout = config.get('system.shutdown_timeout', 15)
        sounds_enabled = "включены" if config.get('sounds.enabled', True) else "выключены"
        default_browser = config.get('media.browser', 'системный')
        current_voice = config.get('voice.edge_voice', 'ru-RU-SvetlanaNeural')
        
        return f"""
📋 ТЕКУЩИЕ НАСТРОЙКИ:

🏙️ Город по умолчанию: {current_city}
🔊 Громкость речи: {speech_volume}%
🎤 Скорость речи: {speech_speed}
⏰ Время до выключения: {shutdown_timeout} сек
🔊 Звуковые эффекты: {sounds_enabled}
🌐 Браузер по умолчанию: {default_browser}
🎙️ Текущий голос: {current_voice}

Команды для изменения:
- "измени город Москва"
- "громкость речи 80" 
- "скорость речи 200"
- "время выключения 30"
- "браузер по умолчанию хром"
- "смени голос на дмитрий"
- "сбрось настройки"
"""
    
    def _handle_calendar_add(self, command):
    
        try:
            # Извлекаем текст после "добавь событие"
            event_text = command.split("добавь событие")[-1].strip()
        
            if not event_text:
                return "Укажите событие: добавь событие встреча 25 декабря 2024 15:30"
        
            # Просто передаем весь текст в calendar_skills
            return calendar_skills.add_event(event_text)
        
        except Exception as e:
            return f"Ошибка добавления события: {e}"
        
    def _handle_voice_list(self):
        try:
            if hasattr(self.voice_engine, 'tts_engine') and hasattr(self.voice_engine.tts_engine, 'get_available_voices'):
                print("🔍 Запрос списка голосов...")
                voices = self.voice_engine.tts_engine.get_available_voices()
                
                if voices:
                    result = "🎯 Доступные русские голосы:\n"
                    voice_names = {
                        'ru-RU-SvetlanaNeural': 'Светлана (женский)',
                        'ru-RU-DmitryNeural': 'Дмитрий (мужской)',
                        'ru-RU-NikitaNeural': 'Никита (мужской)',
                        'ru-RU-DariyaNeural': 'Дария (женский)'
                    }
                    
                    for i, voice in enumerate(voices, 1):
                        display_name = voice_names.get(voice, voice)
                        result += f"{i}. {display_name}\n"
                    
                    result += "\n💡 Скажите 'смени голос на дмитрий' для смены"
                    return result
                else:
                    return "❌ Не удалось получить список голосов"
            else:
                return "❌ Система TTS не доступна"
                
        except Exception as e:
            print(f"❌ Ошибка при получении голосов: {e}")
            return "❌ Ошибка при получении списка голосов"

    def _handle_voice_change(self, command_lower):
        """Обработчик команды смены голоса"""
        voices_map = {
            'светлана': 'ru-RU-SvetlanaNeural',
            'дмитрий': 'ru-RU-DmitryNeural', 
            'никита': 'ru-RU-NikitaNeural',
            'дария': 'ru-RU-DariyaNeural'
        }
        
        for key, voice_id in voices_map.items():
            if key in command_lower:
                if hasattr(self.voice_engine, 'tts_engine'):
                    print(f"Меняю голос на: {key} -> {voice_id}")
                    self.voice_engine.tts_engine.set_voice(voice_id)

                    current_voice = self.voice_engine.tts_engine.voice
                    print(f"Текущий голос после изменения: {current_voice}")
                    return f"Голос изменен на {key}"
        
        return "Доступные голоса: светлана, дмитрий, никита, дария"

    def _get_help_message(self):
        """Возвращает список доступных команд"""
        assistant_name = config.get('assistant.name', 'Пятница')
        default_city = config.get('location.default_city', 'Рязань')

        
        help_text = f"""
🎯 {assistant_name} умеет:

💻 СИСТЕМА:
- 'информация о системе' - показать данные
- 'выключи компьютер' - выключение
- 'перезагрузи компьютер' - перезагрузка  
- 'отмени выключение' - отмена выключения

🔊 ЗВУК:
- 'громкость максимум' - громкость на 100%
- 'громкость тише' - уменьшить громкость
- 'громкость громче' - увеличить громкость
- 'выключи звук' - отключить звук
- 'включи звук' - включить звук

🎵 МЕДИА:
- 'включи музыку' - открыть Hitmo
- 'включи ютуб' - открыть YouTube
- 'пауза' - пауза медиа

⏰ НАПОМИНАНИЯ:
- 'напомни позвонить маме через 10 минут'
- 'поставь таймер на 5 минут'
- 'какие напоминания' - показать напоминания

🌤️ ПОГОДА ({default_city}):
- 'погода' - погода в {default_city}
- 'погода в Москве' - погода в другом городе
- 'температура' - текущая температура

🌐 БРАУЗЕР:
- 'открой браузер' - системный браузер
- 'открой хром' - Chrome
- 'закрой браузер' - закрыть все браузеры
- 'найди кошек' - поиск в интернете

⚙️ НАСТРОЙКИ:
- 'покажи настройки' - текущие настройки
- 'измени город Москва' - сменить город
- 'громкость речи 80' - изменить громкость
- 'скорость речи 200' - изменить скорость
- 'смени голос на дмитрий' - сменить голос
- 'сбрось настройки' - сбросить настройки

🔧 ОТЛАДКА:
- 'отладка голоса' - информация о голосе
- 'текущий голос' - показать текущий голос
- 'используй светлану' - принудительно установить голос
- 'перезагрузи tts' - перезагрузить TTS

📝 ПРОЧЕЕ:
- 'время' - текущее время
- 'дата' - текущая дата
- 'заметка купить молоко' - создать заметку
"""
        return help_text