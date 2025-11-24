# friday_core/brain/smart_command_handler_refactored.py
from friday_core.core.commands.router import CommandRouter
from friday_core.core.commands.processors import (
    AudioCommandProcessor, SystemCommandProcessor, WeatherCommandProcessor,
    MediaCommandProcessor, BasicCommandProcessor, ConfigCommandProcessor
)

class SmartCommandHandlerRefactored:
    """Рефакторенный CommandHandler"""
    
    def __init__(self, config, neuron_orchestrator=None):
        self.config = config
        self.neuron_orchestrator = neuron_orchestrator
        self.router = None
        self._processors = []
    
    def setup_skills(self, basic_skills, system_skills, weather_skills, 
                    media_skills, audio_skills, automation_skills, reminder_skills):
        """Настройка skills (вызывается после их создания)"""
        
        # Создаем обработчики команд
        self._processors = [
            AudioCommandProcessor(audio_skills),
            SystemCommandProcessor(system_skills, self.config),
            WeatherCommandProcessor(weather_skills, self.config),
            MediaCommandProcessor(media_skills),
            BasicCommandProcessor(basic_skills, self.config),
            ConfigCommandProcessor(self.config),
        ]
        
        # Создаем маршрутизатор
        self.router = CommandRouter(self._processors)
        
        # Сохраняем skills для других методов
        self.basic_skills = basic_skills
        self.system_skills = system_skills
        self.weather_skills = weather_skills
        self.media_skills = media_skills
        self.audio_skills = audio_skills
        self.automation_skills = automation_skills
        self.reminder_skills = reminder_skills
        
        print("✅ CommandHandler рефакторен и готов к работе")
    
    def handle_command(self, command: str) -> str:
        """Основной метод обработки команд"""
        if not command:
            return "Не услышал вас, сэр, повторите пожалуйста"
        
        print(f"🎯 Обрабатываю команду: '{command}'")
        
        # Сначала пробуем нейроны (если есть)
        if self.neuron_orchestrator:
            neuron_response = self.neuron_orchestrator.process_command(command)
            if neuron_response is not None:
                print(f"✅ Обработано нейроном: {neuron_response}")
                return neuron_response
        
        # Затем пробуем обычные обработчики
        if self.router:
            return self.router.route(command)
        
        # Запасной вариант
        return "Система обработки команд не инициализирована"
    
    def get_help_message(self) -> str:
        """Получение справки"""
        return """
🎯 Доступные команды:

🔊 Аудио: громкость, тише, громче, выключи звук
💻 Система: выключи компьютер, перезагрузи компьютер  
🌤️ Погода: погода, погода в Москве, температура
🎵 Медиа: включи музыку, включи ютуб
🕒 Базовые: время, дата, привет
⚙️ Настройки: покажи настройки, измени город

Скажите 'помощь' для полного списка команд.
"""