# friday_core/neurons/neuron_orchestrator.py
from typing import List, Optional, Dict, Any, Type
import threading
import time
from friday_core.neurons.base_neuron import BaseNeuron

class NeuronOrchestrator:
    """Оркестратор микроИИ-нейронов"""

    def __init__(self):
        self.neurons: List[BaseNeuron] = []
        self.neuron_classes: Dict[str, Type[BaseNeuron]] = {}
        self._register_neuron_classes()
        self.health_check_thread = None
        self._start_health_monitoring()

        print(f"Оркестратор готов! Доступно: {len(self.neuron_classes)} нейронов для ленивой загрузки")

    
    def _register_neuron_classes(self):
        self.neuron_classes ={
            'AudioNeuron': ('audio_neuron', 'AudioNeuron'),
            'MediaNeuron': ('media_neuron', 'MediaNeuron'),
            'WeatherNeuron': ('weather_neuron', 'WeatherNeuron'),
            'SystemNeuron': ('system_neuron', 'SystemNeuron'),
            'TimeNeuron': ('time_neuron', 'TimeNeuron'),
            'BrowserNeuron': ('browser_neuron', 'BrowserNeuron'),
            'ScreenshotNeuron': ('screenshot_neuron', 'ScreenshotNeuron'),
            'ReminderNeuron': ('reminder_neuron', 'ReminderNeuron')
        }

        print(f"Зарегистрировано {len(self.neuron_classes)} классов нейронов")

    def _load_neuron(self, neuron_name: str) -> Optional[BaseNeuron]:
        if neuron_name not in self.neuron_classes:
            print(f'Нейрон {neuron_name} не зарегистрирован')
            return None
        
        try:
            module_name, class_name = self.neuron_classes[neuron_name]
            module = __import__(f'friday_core.neurons.{module_name}', fromlist=[class_name])
            neuron_class = getattr(module, class_name)
            neuron_instance = neuron_class()
            self.neurons.append(neuron_instance)
            print(f'Ленивая загрузка {neuron_name}')
            return neuron_instance
        
        except Exception as e:
            print(f'Ошибка загрузки нейрона {neuron_name}: {e}')
            return None
        
    def _get_or_load_neuron(self, neuron_type: str) -> Optional[BaseNeuron]:
        for neuron in self.neurons:
            if neuron.__class__.__name__ == neuron_type:
                return neuron
            
        return self._load_neuron(neuron_type)
    
    def process_command(self, command: str) -> Optional[str]:
        if not command:
            return None

        print(f'Оркестратор ищет нейрон для: "{command}"')
        command_lower = command.lower()

        neuron_mapping = {
            'audio': ['громкость', 'звук', 'тише', 'громче', 'выключи звук'],
            'weather': ['погода', 'температура', 'градус', 'на улице'],
            'time': ['время', 'час', 'который час', 'дата', 'число'],
            'system': ['выключи', 'перезагрузи', 'компьютер', 'система'],
            'media': ['музыка', 'включи', 'песня', 'ютуб', 'youtube'],
            'browser': ['открой', 'браузер', 'интернет', 'найди', 'поиск'],
            'screenshot': ['скриншот', 'снимок', 'скрин'],
            'reminder': ['напомни', 'таймер', 'напоминание']
        }

        target_neuron = None
        for neuron_type, keywords in neuron_mapping.items():
            if any(keyword in command for keyword in keywords):
                target_neuron = neuron_type
                break

        if not target_neuron:
            print(f'Не определен подходящий нейрон для "{command}"')
            return None

        neurom_class_name = target_neuron.title() + 'Neuron'

        neuron = self._get_or_load_neuron(neurom_class_name)
        if not neuron:
            return f'Нейрон "{neurom_class_name}" не доступен'

        if not neuron.is_active:
            return f'Нейрон "{neuron.name}" отключен'
        
        result = neuron.handle_safely(command)
        if result is not None:
            print(f'Нейрон "{neuron.name}" обработал команду')
            return result

        print(f'Нейрон "{neuron.name}" не смог обработать  "{command}"')
        return None

    def get_status(self):
        status = {
            'total_registered': len(self.neuron_classes),
            'total_loaded': len(self.neurons),
            'active': 0,
            'inactive': 0,
            'details': {},
            'available_neurons': list(self.neuron_classes.keys())
        }

        for neuron in self.neurons:
            is_active = neuron.is_active
            status['details'][neuron.name] = {
                'active': is_active,
                'errors': neuron.error_count,
                'class': neuron.__class__.__name__
            }

            if is_active:
                status['active'] += 1
            else:
                status['inactive'] += 1

        return status
    
    def _start_health_monitoring(self):
        def health_check():
            while True:
                time.sleep(60)
                if self.neurons:
                    active_neurons = sum(1 for n in self.neurons if n.is_active)
                    total_neurons = len(self.neurons)

                    print(f'Статус нейронов: {active_neurons}/{total_neurons} активны(загружено{total_neurons}/{len(self.neuron_classes)})')

        self.health_check_thread = threading.Thread(target=health_check, daemon=True)
        self.health_check_thread.start()

    def restart_neuron(self, neuron_name: str) -> bool:
        neuron = self._get_or_load_neuron(neuron_name)
        if neuron:
            neuron.is_active = True
            neuron.error_count = 0
            print(f'Нейрон "{neuron.name}" перезапущен')
            return True
        print(f'Нейрон "{neuron.name}" не перезапущен')
        return False

    def restart_all_neurons(self) -> str:
        restarted = 0
        for neuron in self.neurons:
            if not neuron.is_active:
                neuron.is_active = True
                neuron.error_count = 0
                restarted += 1
        return f'Перезапущено {restarted} нейронов (из {len(self.neurons)} загруженных)'
    
    def force_load_all_neurons(self):
        print('Принудительная перезагрузка всех нейронов')
        for neuron_name in self.neuron_classes.keys():
            self._load_neuron(neuron_name)
        print(f'Загружено {len(self.neurons)} нейронов')


