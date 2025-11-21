# main.py
from friday_core.engine.voice_engine import VoiceEngine
from friday_core.brain.command_handler import CommandHandler
from friday_core.engine.sound_manager import sound_manager
from friday_core.config.config import config
import time
import sys
import re
from friday_core.brain.smart_command_handler import SmartCommandHandler
from friday_core.utills.recomendation_system import recomendation_system
from friday_core.utills.event_bus import event_bus
from test_event_subscribers import test_subscribers
from friday_core.utills.logger import perfomance_logger
from friday_core.brain.optimized_smart_command import OptimizedSmartCommand
from friday_core.utills.health_monitor import HealthMonitor

class Friday:
    def __init__(self):
        print("🔧 Инициализация Пятницы...")
        self.voice_engine = VoiceEngine()

        self.perfomance_logger = perfomance_logger
        self.command_handler = OptimizedSmartCommand()
        self.health_monitor = HealthMonitor()


        self.voice_engine._init_recognizer()
        
        self.command_handler = SmartCommandHandler()
        self.is_running = False

        self.health_monitor.start_monitoring()
        print(f"Event Bus: Статистика {event_bus.get_stats()}")
        self.assistant_name = config.get('assistant.name', 'Пятница')

        from friday_core.config.personalization import personalization
        self.personalization = personalization

        print("✅ Пятница инициализирована")

    
    def _count_commands(self):
        """Подсчитывает количество доступных команд"""
        # Примерная оценка количества команд
        return "50+"
    
    def _process_command(self, command):
        print(f'🎯 Голосовая команда: "{command}"')
        start_time = time.time()
    
        try:

            recomendation_system.record_command(command)

            response = self.command_handler.handle_command(command)
            processing_time = time.time() - start_time
            

            if self._should_show_recomendations():
                rects = recomendation_system.get_recomendations(2)
                if rects:
                    print("💡 Рекомендации:", ", ".join(rects))
            
            # 🔥 ПРОВЕРКА НА КОМАНДУ ВЫХОДА
            if self._is_exit_command(response, command):
               self.shutdown()
               return False

            # Звуковой сигнал
            if 'ошибка' not in response.lower() and 'не поняла' not in response.lower():
                sound_manager.play_success()
            else:
                sound_manager.play_error() 
            
            # Озвучка
            print(f"💬 Ответ: {response}")
            self.voice_engine.speak(response)
            
            time.sleep(1)
            
            if processing_time > 0.5:  # больше 500ms
                self.performance_logger.logger.warning(
                    f"Slow command processing: '{command}' took {processing_time:.2f}s"
                )
                
            return response
            
        except Exception as e:
            print(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
            
            # Пытаемся сообщить об ошибке
            try:
                self.voice_engine.speak("Произошла критическая ошибка, проверьте консоль")
            except:
                pass
                
            time.sleep(2)
            
            processing_time = time.time() - start_time
            self.performance_logger.logger.error(
                f"Command failed: '{command}' - {str(e)}"
            )
            return "Произошла ошибка при обработке команды"
        
    def get_system_status(self):
        return {
            "performance": self.performance_logger.get_performance_stats(),
            "health": self.health_monitor.get_health_report(),
            "neurons": self.command_handler.neuron_orchestrator.get_status(),
            "uptime": time.time() - self.start_time if hasattr(self, 'start_time') else 0
        }
        
    def _should_show_recomendations(self):
        import random
        return random.random() < 0.2
        
    
    def _handle_error(self, error):
        """Обрабатывает ошибки в основном цикле"""
        print(f'💥 Ошибка в основном цикле: {error}')
        import traceback
        traceback.print_exc()
        time.sleep(2)
    
    def _graceful_shutdown(self):
        """Корректное завершение работы при прерывании"""
        print("\n🛑 Получен сигнал прерывания")
        self.shutdown()

    def start(self):
        """Запускает основную петлю"""
        self.is_running = True
        
        sound_manager.play_startup()
        
        # Приветственное сообщение
        user_name = self.personalization.get_user_name()
        welcome_msg = f"""
🤖 {self.assistant_name} активирована
🎯 Пользователь: {user_name}
💡 Доступно команд: {self._count_commands()}
🔧 Система готова к работе"""
        print(welcome_msg)

        greeting = self.personalization.get_personalized_greeting()
        
        self.voice_engine.speak(greeting + ' готова к работе')
        
        # Основной цикл
        try:
            while self.is_running:
                try:
                   
                   if self.voice_engine.active_session:
                       time_left = self.voice_engine.session_timeout - (time.time() - self.voice_engine.last_command_time)
                       if time_left > 0:
                           print(f'\nАктивная сессия - осталось {int(time_left)} сек')

                   command = self.voice_engine.smart_listen()
                   
                   if command and command not in['', 'не расслышала', 'ошибка']:
                       if not self._process_command(command):
                           break
                       
                   elif command in ['не расслышала', 'ошибка']:
                       if self.voice_engine.active_session:
                           self.voice_engine.speak('Повторите, пожалуйста')
                       else:
                           print('ошибка распознавания')
                       time.sleep(1)

                except KeyboardInterrupt:
                    self._graceful_shutdown()
                    break
                except Exception as e:
                    self._handle_error(e)
        
        finally:
            self.cleanup()

    def _is_exit_command(self, response, original_command):
        """Проверяет, является ли команда командой выхода"""
        exit_phrases = [
            'до свидания', 'выход', 'стоп', 'заверши', 'пока', 
            'завершить работу', 'отключись', 'отдыхай'
        ]
        
        # Проверяем по ответу и оригинальной команде
        response_lower = response.lower()
        command_lower = original_command.lower()

        print(f'Отладка выхода: command="{command_lower}", response="{response_lower}"')
        
        echnical_responses = [
        'скриншот', 'снимок', 'файл', 'папка', 'сохранен',
        'сделано', 'открываю', 'показываю', 'статистика'
    ]
    
        command_lower = original_command.lower()
        exit_command = any(
            re.search(r'\b' + re.escape(phrase) + r'\b', command_lower)
            for phrase in exit_phrases
        )

        if exit_command:
            print(f'Обнаружена команда выхода: {command_lower}')
            self.voice_engine._end_session()
        
            return True
        print('Это не команда выхода')
        return False
    

    def shutdown(self):
        """Корректное завершение работы"""
        print("\n🛑 Завершение работы Пятницы...")
        self.voice_engine.speak('До свидания, сэр! Жду вашего возвращения.')
        sound_manager.play_shutdown()
        self.is_running = False

    def cleanup(self):
        """Очистка ресурсов"""
        print(f"👋 {self.assistant_name} завершает работу")
        # Дополнительная очистка если нужна

def main():
    print("🎯 Запуск Пятницы...")
    try:
        friday = Friday()
        friday.start()
    except Exception as e:
        print(f"💥 Фатальная ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("🏁 Программа завершена")
        # Гарантированно завершаем программу
        sys.exit(0)

if __name__ == "__main__":
    main()