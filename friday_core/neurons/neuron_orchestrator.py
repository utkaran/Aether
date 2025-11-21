# friday_core/neurons/neuron_orchestrator.py
from typing import List, Optional, Dict, Any
import threading
import time
from .base_neuron import BaseNeuron

class NeuronOrchestrator:
    """Оркестратор микроИИ-нейронов"""

    def __init__(self):
        self.neuron_registry: List[Dict[str, Any]] = []
        self.active_neurons: List[BaseNeuron] = []
        self._load_neuron_registry()
        self.health_check_thread = None
        self._start_health_monitoring()

        print(f"Оркестратор зарегистрировал {len(self.neuron_registry)} нейронов (ленивая загрузка)")

    def _load_neuron_registry(self):
        neurons_to_register = [
            {
                'module': 'weather_neuron',
                'class': 'weather_neuron',
                'keywords': ['погода', 'температура', 'градус', 'дождь', 'солнце', 'на улице', 'мороз', 'жара', 'прогноз'],
                'instance': None
            },

            {
                'module': 'system_neuron', 
                'class': 'SystemNeuron',
                'keywords': ['выключи', 'перезагрузи', 'компьютер', 'система', 'отмени выключение', 'перезагрузка', 'выключение'],
                'instance': None
            },

            {
                'module': 'time_neuron',
                'class': 'TimeNeuron', 
                'keywords': ['время', 'час', 'времени', 'который час', 'дата', 'число', 'какое число', 'сегодня', 'сколько времени'],
                'instance': None
            },

            {
                'module': 'media_neuron',
                'class': 'MediaNeuron',
                'keywords': ['музыка', 'включи', 'песня', 'hitmo', 'ютуб', 'youtube', 'пауза', 'пауз', 'плэйлист', 'видео', 'медиа'],
                'instance': None
            },

            {
                'module': 'audio_neuron',
                'class': 'AudioNeuro',
                'keywords': ['громкость', 'звук', 'тише', 'громче', 'максимум', 'полная громкость', 'выключи звук', 'без звука', 'включи звук'],
                'instance': None
            },

            {
                 'module': 'reminder_neuron', 
                'class': 'ReminderNeuron',
                'keywords': ['напомни', 'таймер', 'напоминание', 'напоминай', 'поставь таймер', 'поставить таймер'],
                'instance': None
            },

            {
                
                'module': 'browser_neuron',
                'class': 'BrowserNeuron',
                'keywords': ['открой', 'запусти', 'браузер', 'интернет', 'найди', 'поиск', 'закрой', 'приложение', 'программа', 'хром', 'firefox', 'edge'],
                'instance': None
            },

            {
                'module': 'screenshot_neuron',
                'class': 'ScreenshotNeuron', 
                'keywords': ['скриншот', 'снимок', 'скрин', 'сними', 'сделай скриншот'],
                'instance': None
            }
        ]

        self.neuron_registry = neurons_to_register  
        print(f'Зарегистрировано {len(self.neuron_registry)} нейронов для ленивой загрузки')

    def _get_neuron_instance(self, neuron_info: Dict[str, Any]) -> Optional[BaseNeuron]:
        if neuron_info['instance'] is not None:
            return neuron_info['instance']
    
        try:
            module_name = neuron_info['module']  # 'weather_neuron'
            class_name = neuron_info['class']    # 'WeatherNeuron'

            print(f"🔍 Загружаю нейрон: {module_name}.{class_name}")

            # ПРАВИЛЬНЫЙ способ импорта
            import importlib
            full_module_path = f'friday_core.neurons.{module_name}'
            module = importlib.import_module(full_module_path)

            # Получаем класс из модуля
            neuron_class = getattr(module, class_name)

            # Создаем экземпляр
            neuron_instance = neuron_class()

            # Сохраняем созданный экземпляр
            neuron_info['instance'] = neuron_instance
            self.active_neurons.append(neuron_instance)

            print(f"🚀 Лениво загружен нейрон: {class_name}")
            return neuron_instance
        
        except Exception as e:
            print(f"❌ Не удалось загрузить {neuron_info['class']}: {e}")
            import traceback
            print(f"🔍 Детали ошибки: {traceback.format_exc()}")
            return None
        
    def _find_potential_neurons(self, command: str) -> List[Dict[str, Any]]:
        command_lower = command.lower()
        potential_neurons = []

        for neuron_info in self.neuron_registry:
            if any(keyword in command_lower for keyword in neuron_info['keywords']):
                potential_neurons.append(neuron_info)

        return potential_neurons
    
    def process_command(self, command: str) -> Optional[str]:
        if not command:
            return None
        
        print(f"🎯 Оркестратор ищет нейрон для: '{command}'")

        # Быстрый поиск подходящих нейронов по ключевым словам
        potential_neurons = self._find_potential_neurons(command)

        if not potential_neurons:
            print(f"🔍 Ни один нейрон не подходит по ключевым словам для: '{command}'")
            return None
        
        print(f"Найдено {len(potential_neurons)} потенциальных нейронов")

        # Проверяем подходящие нейроны (загружая их)

        for neuron_info in potential_neurons:
            neuron = self._get_neuron_instance(neuron_info)

            if neuron is None or not neuron.is_active:
                continue

            result = neuron.handle_safely(command)
            if result is not None:
                print(f"✅ Нейрон '{neuron.name}' обработал команду")
                return result
            
        print(f"Подходящие нейроны не смогли обработать: '{command}'")
        return None
    
    def _start_health_monitoring(self):
        def health_check():
            while True:
                time.sleep(60)
                active_count = sum(1 for n in self.active_neurons if n.is_active)
                total_loaded = len(self.active_neurons)
                total_registered = len(self.neuron_registry)

                print(f'Статус нейронов: {active_count}/{total_loaded} активны (всего зарегистрировано: {total_registered})"')

                for neuron in self.active_neurons:
                    status = "🟢" if neuron.is_active else "🔴"
                    print(f'   {status} {neuron.name} (ошибок: {neuron.error_count})')

                lazy_neurons = [n for n in self.neuron_registry if n['instance'] is None]
                if lazy_neurons:
                    print(f'Загруженные нейроны: {len(lazy_neurons)}')
                    for neuron_info in lazy_neurons:
                        print(f'  {neuron_info["class"]} (ждет команды)')
        
        self.health_check_thread = threading.Thread(target=health_check, daemon=True)
        self.health_check_thread.start()

    def get_status(self):
        loaded_neurons = [n for n in self.neuron_registry if n['instance'] is not None]
        lazy_neurons = [n for n in self.neuron_registry if n['instance'] is None]

        active_loaded = sum(1 for n in loaded_neurons if n['instance'].is_active)

        status = {
            'total_registered': len(self.neuron_registry),
            'total_loaded': len(loaded_neurons),
            'total_lazy': len(lazy_neurons),
            'active_loaded': active_loaded,
            'inactive_loaded': len(loaded_neurons) - active_loaded,
            'details': {}
        }

        for neuron_info in self.neuron_registry:
            if neuron_info['instance'] is not None:
                neuron = neuron_info['instance']
                status['details'][neuron.name] = {
                    'loaded': True,
                    'active': neuron.is_active,
                    'errors': neuron.error_count
                }
            else:
                status['details'][neuron_info['class']] = {
                    'loaded': False,
                    'active': False,
                    'errors': 0
                }
        return status
    
    def restart_neuron(self, neuron_name: str) -> bool:
        for neuron_info in self.neuron_registry:
            if neuron_info['instance'] is not None and neuron_info['instance'].name == neuron_name:
                neuron = neuron_info['instance']
                neuron.is_active = True
                neuron.error_count = 0
                print(f"Нейрон '{neuron_name}' перезапущен")
                return True
            
        print(f"Нейрон '{neuron_name}' не найден или не загружен")
        return False
    
    def restart_all_neurons(self) -> str:
        restarted = 0
        for neuron_info in self.neuron_registry:
            if neuron_info['instance'] is not None and not neuron_info['instance'].is_active:
                neuron_info['instance'].is_active = True
                neuron_info['instance'].error_count = 0
                restarded += 1

        return f"Перезапущено {restarted} загруженных нейронов"
    
    def force_load_all_neurons(self):
        print("Принудительная загрузка всех нейронов...")
        for neuron_info in self.neuron_registry:
            if neuron_info['instance'] is None:
                self._get_neuron_instance(neuron_info)

        print(f"✅ Все {len(self.neuron_registry)} нейронов загружены")

    def get_loaded_neurons_count(self) -> int:
        return len([n for n in self.neuron_registry if n['instance']] is not None)
    
    def get_lazy_neurons_info(self) -> List[str]:
        lazy_neurons = [n for n in self.neuron_registry if n['instance'] is None]
        return [f"{neuron_info['class']} ({neuron_info['module']})" for neuron_info in lazy_neurons]
