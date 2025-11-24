# friday_core/skills/automation_skills.py
import pyautogui
import psutil
import os
import subprocess
import time
import pyperclip
from datetime import datetime
import webbrowser
from pathlib import Path

class AutomationSkills:
    def __init__(self):
        # Настройки безопасности pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # Создаем папку для скриншотов
        self.screenshots_dir = Path("Screenshots")
        self._setup_screenshots_folder()
        
        # Словарь приложений для быстрого доступа
        self.applications = {
            # Microsoft Office
            'word': 'winword',
            'вёрд': 'winword',
            'excel': 'excel',
            'эксель': 'excel',
            'powerpoint': 'powerpnt',
            'пауэрпоинт': 'powerpnt',
            'outlook': 'outlook',
            
            # Системные приложения
            'блокнот': 'notepad',
            'калькулятор': 'calc',
            'кальк': 'calc',
            'проводник': 'explorer',
            'панель управления': 'control',
            'диспетчер задач': 'taskmgr',
            'пайнт': 'mspaint',
            'краска': 'mspaint',
            
            # Браузеры
            'хром': 'chrome',
            'google chrome': 'chrome',
            'файрфокс': 'firefox',
            'firefox': 'firefox',
            'edge': 'msedge',
            'эдж': 'msedge',
            'опера': 'opera',
            'opera': 'opera',
            'яндекс': 'browser.exe', 
            'yandex': 'browser.exe',
            'yandex.browser': 'browser.exe',
            
            # Мессенджеры
            'телеграм': 'telegram',
            'telegram': 'telegram',
            'дискорд': 'discord',
            'discord': 'discord',
            'ватсап': 'whatsapp',
            'whatsapp': 'whatsapp',
            
            # Другое
            'вк': 'vk',
            'видеоплеер': 'wmplayer',
            'плеер': 'wmplayer'
        }
        
        # Горячие клавиши для управления
        self.hotkeys = {
            'скриншот': ['win', 'prtscr'],
            'скриншот области': ['win', 'shift', 's'],
            'поиск': ['win', 's'],
            'выполнить': ['win', 'r'],
            'параметры': ['win', 'i'],
            'центр уведомлений': ['win', 'a'],
            'проводник': ['win', 'e']
        }

    def _setup_screenshots_folder(self):
      try:
          # Создаем основную папку Screenshots в текущей директории
          self.screenshots_dir = Path.cwd() / "Screenshots"
          self.screenshots_dir.mkdir(exist_ok=True)
          
          # Создаем подпапки по годам и месяцам
          current_year = datetime.now().strftime("%Y")
          current_month = datetime.now().strftime("%m_%B")
          
          year_dir = self.screenshots_dir / current_year
          month_dir = year_dir / current_month
          
          year_dir.mkdir(exist_ok=True)
          month_dir.mkdir(exist_ok=True)
          
          # Устанавливаем текущую папку для скриншотов
          self.current_screenshots_dir = month_dir
          
          print(f"📁 Папка для скриншотов: {self.current_screenshots_dir}")
          
      except Exception as e:
          print(f"❌ Ошибка создания папки для скриншотов: {e}")
          # Резервный вариант - использовать основную папку
          self.current_screenshots_dir = self.screenshots_dir

    def _get_screenshot_filename(self, prefix="screenshot"):
        """Генерирует имя файла для скриншота"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{prefix}_{timestamp}.png"
        return self.current_screenshots_dir / filename

    def _get_relative_path(self, file_path):
        """Безопасно получает относительный путь"""
        try:
            # Пробуем получить относительный путь
            return file_path.relative_to(Path.cwd())
        except ValueError:
            # Если не получается (разные диски и т.д.), возвращаем абсолютный путь
            return file_path

    def take_screenshot(self, area=False, description=""):
        """Сделать скриншот с сохранением в организованную папку"""
        try:
            # Обновляем путь к текущей папке (на случай смены дня/месяца)
            self._setup_screenshots_folder()
            
            if area:
                # Скриншот области (используем системное средство Windows)
                pyautogui.hotkey('win', 'shift', 's')
                return "📸 Готовлюсь к созданию скриншота области... Используйте выделение."
            else:
                # Полный скриншот
                if description:
                    prefix = description.replace(" ", "_").lower()[:20]
                else:
                    prefix = "screenshot"
                
                filename = self._get_screenshot_filename(prefix)
                screenshot = pyautogui.screenshot()
                screenshot.save(filename)
                
                # Безопасно получаем путь для отображения
                display_path = self._get_relative_path(filename)
                return f"📸 Скриншот сохранен: {display_path}"

        except Exception as e:
            return f"❌ Ошибка при создании скриншота: {e}"

    def take_multiple_screenshots(self, count=3, delay=2):
        """Сделать несколько скриншотов с задержкой"""
        try:
            print(f'начинаю создание {count} скриншотов...')
            results = []
            self._setup_screenshots_folder()
            for i in range(count):
                if i > 0:
                    time.sleep(delay)
                
                filename = self._get_screenshot_filename(f"series_{i+1}")
                screenshot = pyautogui.screenshot()
                screenshot.save(str(filename))
                
                display_name = filename.name
                results.append(str(display_name))

                if i < count -1:
                    time.sleep(0.5)
            result_text = f"📸 Сделано {count} скриншотов:\n" + "\n".join([f"{i+1}. {name}" for i, name in enumerate(results)])
            return result_text
            
        except Exception as e:
            return f"❌ Ошибка при создании серии скриншотов: {e}"

    def open_screenshots_folder(self):
        """Открыть папку со скриншотами"""
        try:
            # Используем абсолютный путь для открытия
            absolute_path = self.current_screenshots_dir.resolve()
            os.startfile(str(absolute_path))
            display_path = self._get_relative_path(absolute_path)
            return f"📁 Открываю папку со скриншотами: {display_path}"
        except Exception as e:
            return f"❌ Не удалось открыть папку: {e}"

    def list_recent_screenshots(self, count=5):
        """Показать последние скриншоты"""
        
        try:
            
            print(f"🔍 Ищу последние {count} скриншотов...")
            # Используем абсолютный путь для поиска
            absolute_dir = self.current_screenshots_dir.resolve()
            print(f'ищу в папке : {absolute_dir}')

            if not absolute_dir.exists():
                print('Папка не существует')
                return 'Папка скригшотов не существует'

            screenshot_files = list(absolute_dir.glob("*.png"))
            
            # Сортируем по дате изменения (новые сначала)
            screenshot_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            print(f"📄 Найдено файлов: {len(screenshot_files)}")

            screenshot_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            if not screenshot_files:
                return "📁 В папке скриншотов пока нет файлов"
            
            result = f"📸 Последние {min(count, len(screenshot_files))} скриншотов:\n"
            for i, file_path in enumerate(screenshot_files[:count]):
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                time_str = file_time.strftime("%d.%m.%Y %H:%M")
                display_name = self._get_relative_path(file_path)
                result += f"{i+1}. {display_name.name} ({time_str})\n"
            print('Список скриншотов восстановлен')
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Ошибка при получении списка скриншотов: {e}"
            print(error_msg)
            import traceback
            traceback.print_exc()  # Печатаем полную трассировку ошибки
            return error_msg

    def cleanup_old_screenshots(self, days=30):
        """Удалить старые скриншоты"""
        try:
            cutoff_time = time.time() - (days * 24 * 60 * 60)
            deleted_count = 0
            
            # Используем абсолютный путь для поиска
            absolute_dir = self.screenshots_dir.resolve()
            
            # Рекурсивно ищем все PNG файлы в папке Screenshots
            for file_path in absolute_dir.rglob("*.png"):
                if file_path.stat().st_mtime < cutoff_time:
                    try:
                        file_path.unlink()
                        deleted_count += 1
                    except Exception as e:
                        print(f"Не удалось удалить {file_path}: {e}")
            
            return f"🗑️ Удалено {deleted_count} скриншотов старше {days} дней"
            
        except Exception as e:
            return f"❌ Ошибка при очистке скриншотов: {e}"

    def get_screenshots_stats(self):
        """Статистика по скриншотам"""
        try:
            total_files = 0
            total_size = 0
            by_month = {}
            
            # Используем абсолютный путь для поиска
            absolute_dir = self.screenshots_dir.resolve()
            
            # Считаем все PNG файлы рекурсивно
            for file_path in absolute_dir.rglob("*.png"):
                total_files += 1
                total_size += file_path.stat().st_size
                
                # Группируем по месяцам
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                month_key = file_time.strftime("%Y-%m")
                by_month[month_key] = by_month.get(month_key, 0) + 1
            
            total_size_mb = total_size / (1024 * 1024)
            
            stats = f"""
    📊 СТАТИСТИКА СКРИНШОТОВ:

    📁 Всего файлов: {total_files}
    💾 Общий размер: {total_size_mb:.1f} МБ
    📅 Распределение по месяцам:
    """
            for month, count in sorted(by_month.items()):
                stats += f"  • {month}: {count} скриншотов\n"
            
            display_path = self._get_relative_path(self.current_screenshots_dir)
            stats += f"\n📂 Текущая папка: {display_path}"
            
            return stats
            
        except Exception as e:
            return f"❌ Ошибка при получении статистики: {e}"
        
    def safe_screenshot_operation(self, operation_name, operation_func):
      try:
          print(f"🔧 Выполняю операцию: {operation_name}")
          self._setup_screenshots_folder()
          return operation_func()
      except Exception as e:
          error_msg = f"❌ Ошибка в операции '{operation_name}': {e}"
          print(error_msg)
          import traceback
          traceback.print_exc() 
          return error_msg

    def open_application(self, app_name):
        """Открытие приложений по имени"""
        app_name_lower = app_name.lower()
        
        # Поиск в словаре приложений
        for key, value in self.applications.items():
            if app_name_lower in key or key in app_name_lower:
                try:
                    if value in ['chrome', 'firefox', 'msedge', 'opera']:
                        # Браузеры открываем через webbrowser для корректной работы
                        webbrowser.get(value).open('')
                    else:
                        os.system(f"start {value}")
                    
                    return f"Открываю {key}"
                except Exception as e:
                    return f"❌ Не удалось открыть {key}: {e}"
        
        # Если приложение не найдено в словаре, пробуем открыть напрямую
        try:
            os.system(f"start {app_name}")
            return f"Пытаюсь открыть {app_name}"
        except:
            return f"Приложение '{app_name}' не найдено"

    def close_application(self, app_name):
        """Закрытие приложений"""
        app_name_lower = app_name.lower()
        
        # Сопоставление имен процессов
        process_names = {
            'word': 'WINWORD.EXE',
            'excel': 'EXCEL.EXE',
            'powerpoint': 'POWERPNT.EXE',
            'notepad': 'notepad.exe',
            'блокнот': 'notepad.exe', 'notepad': 'notepad.exe',
            'калькулятор': 'Calculator.exe', 'calc': 'Calculator.exe', 'кальк': 'Calculator.exe',
            'проводник': 'explorer.exe', 'explorer': 'explorer.exe',
            'панель управления': 'control.exe', 'control': 'control.exe',
            'диспетчер задач': 'Taskmgr.exe', 'taskmgr': 'Taskmgr.exe', 'taskmanager': 'Taskmgr.exe',
            'пайнт': 'mspaint.exe', 'краска': 'mspaint.exe', 'paint': 'mspaint.exe', 'mspaint': 'mspaint.exe',
            
            # Браузеры
            'хром': 'chrome.exe', 'chrome': 'chrome.exe', 'google chrome': 'chrome.exe',
            'файрфокс': 'firefox.exe', 'firefox': 'firefox.exe',
            'edge': 'msedge.exe', 'эдж': 'msedge.exe', 'microsoft edge': 'msedge.exe', 'msedge': 'msedge.exe',
            'опера': 'opera.exe', 'opera': 'opera.exe',
            'яндекс': 'browser.exe', 'yandex': 'browser.exe',
            
            # Мессенджеры
            'телеграм': 'telegram.exe', 'telegram': 'telegram.exe',
            'дискорд': 'discord.exe', 'discord': 'discord.exe',
            'ватсап': 'whatsapp.exe', 'whatsapp': 'whatsapp.exe',
            'скайп': 'skype.exe', 'skype': 'skype.exe',
            
            # Другое
            'вк': 'vk.exe', 'vk': 'vk.exe',
            'видеоплеер': 'wmplayer.exe', 'плеер': 'wmplayer.exe', 'media player': 'wmplayer.exe', 'wmplayer': 'wmplayer.exe',
            'камера': 'camera.exe', 'camera': 'camera.exe',
            'календарь': 'calendar.exe', 'calendar': 'calendar.exe',
            'почта': 'mail.exe', 'mail': 'mail.exe'
        }

        target_process = None
        display_name = app_name
        
        if app_name_lower in process_names:
            target_process = process_names[app_name_lower]
            display_name = app_name_lower
        else:
            for key, process in process_names.items():
                if key in app_name_lower:
                    target_process = process
                    display_name = key
                    break
        
        if not target_process:
            return f"Приложение '{app_name}' не найдено"
        
        # ЗАКРЫВАЕМ ЧЕРЕЗ PSUTIL (надежный способ)
        try:
            closed_count = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() == target_process.lower():
                        proc.terminate()  # Сначала мягко закрываем
                        closed_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            if closed_count > 0:
                # Даем время на закрытие
                time.sleep(1)
                
                # Проверяем, остались ли процессы
                still_running = 0
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] and proc.info['name'].lower() == target_process.lower():
                        still_running += 1
                
                if still_running > 0:
                    # Если не закрылось - принудительно убиваем
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            if proc.info['name'] and proc.info['name'].lower() == target_process.lower():
                                proc.kill()
                        except:
                            pass
                    
                    return
                else:
                    return f"Закрываю {display_name}"
            else:
                return f"Приложение '{display_name}' не запущено"
                
        except Exception as e:
            return f"Ошибка при закрытии {display_name}: {e}"

    def get_system_resources(self):
        """Мониторинг ресурсов системы"""
        try:
            # Загрузка CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Использование памяти
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_gb = memory.used / (1024**3)
            memory_total_gb = memory.total / (1024**3)
            
            # Использование диска
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free_gb = disk.free / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            
            # Температура (если доступно)
            try:
                temps = psutil.sensors_temperatures()
                cpu_temp = "N/A"
                if 'coretemp' in temps:
                    cpu_temp = max([temp.current for temp in temps['coretemp']])
            except:
                cpu_temp = "N/A"
            
            report = f"""
💻 СИСТЕМНЫЕ РЕСУРСЫ:

⚡ ЦПУ: {cpu_percent}% загружено
💾 Память: {memory_percent}% ({memory_used_gb:.1f}ГБ / {memory_total_gb:.1f}ГБ)
💿 Диск C: {disk_percent}% свободно {disk_free_gb:.1f}ГБ из {disk_total_gb:.1f}ГБ
🌡️ Температура ЦПУ: {cpu_temp}°C
"""
            return report
            
        except Exception as e:
            return f"❌ Ошибка получения системной информации: {e}"

    def window_management(self, action):
        """Управление окнами"""
        try:
            actions = {
                'сверни все': lambda: pyautogui.hotkey('win', 'd'),
                'сверни все окна': lambda: pyautogui.hotkey('win', 'd'),
                'покажи рабочий стол': lambda: pyautogui.hotkey('win', 'd'),
                'переключи окно': lambda: pyautogui.hotkey('alt', 'tab'),
                'следующее окно': lambda: pyautogui.hotkey('alt', 'tab'),
                'закрой окно': lambda: pyautogui.hotkey('alt', 'f4'),
                'закрой приложение': lambda: pyautogui.hotkey('alt', 'f4'),
                'разверни окно': lambda: pyautogui.hotkey('win', 'up'),
                'восстанови окно': lambda: pyautogui.hotkey('win', 'down'),
                'сверни окно': lambda: pyautogui.hotkey('win', 'down') + pyautogui.hotkey('win', 'down')
            }
            
            if action in actions:
                actions[action]()
                return f"✅ {action.replace('сверни все', 'Рабочий стол показан').replace('переключи', 'Переключаю').replace('закрой', 'Закрываю').replace('разверни', 'Разворачиваю').replace('восстанови', 'Восстанавливаю').replace('сверни', 'Сворачиваю')}"
            else:
                return f"❌ Действие '{action}' не поддерживается"
                
        except Exception as e:
            return f"❌ Ошибка управления окнами: {e}"

    def type_text(self, text):
        """Ввод текста в текущее активное окно"""
        try:
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            return f"✅ Текст введен: {text[:50]}{'...' if len(text) > 50 else ''}"
        except Exception as e:
            return f"❌ Ошибка ввода текста: {e}"

    def press_key(self, key_name):
        """Нажатие клавиши или комбинации"""
        try:
            key_mapping = {
                'enter': 'enter',
                'энтер': 'enter',
                'пробел': 'space',
                'таб': 'tab',
                'эскейп': 'esc',
                'escape': 'esc',
                'удалить': 'delete',
                'делит': 'delete',
                'бэкспейс': 'backspace'
            }
            
            if key_name in key_mapping:
                pyautogui.press(key_mapping[key_name])
                return f"✅ Нажата клавиша {key_name}"
            else:
                # Пробуем нажать как есть
                pyautogui.press(key_name)
                return f"✅ Нажата клавиша {key_name}"
                
        except Exception as e:
            return f"❌ Ошибка нажатия клавиши: {e}"

    def hotkey_combination(self, keys):
        """Выполнение комбинации горячих клавиш"""
        try:
            key_list = keys.split()
            pyautogui.hotkey(*key_list)
            return f"✅ Выполнена комбинация: {keys}"
        except Exception as e:
            return f"❌ Ошибка выполнения комбинации: {e}"

    def get_battery_status(self):
        """Получение информации о батарее"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = battery.power_plugged
                time_left = battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "∞"
                
                status = "🔌 Подключено к сети" if plugged else "🔋 Работает от батареи"
                if time_left != "∞":
                    hours = time_left // 3600
                    minutes = (time_left % 3600) // 60
                    time_str = f"{hours}ч {minutes}м"
                else:
                    time_str = "не ограничено"
                
                return f"🔋 Батарея: {percent}%\n{status}\n⏱️ Осталось: {time_str}"
            else:
                return "❌ Информация о батарее недоступна"
                
        except Exception as e:
            return f"❌ Ошибка получения информации о батарее: {e}"

    def list_running_processes(self, top=5):
        """Показать самые ресурсоемкие процессы"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            # Сортируем по использованию памяти
            processes.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
            
            result = "🏃 ТОП-5 процессов по памяти:\n"
            for i, proc in enumerate(processes[:top]):
                result += f"{i+1}. {proc['name']}: {proc['memory_percent'] or 0:.1f}% памяти\n"
            
            return result
            
        except Exception as e:
            return f"❌ Ошибка получения списка процессов: {e}"

    def create_shortcut(self, target_path, shortcut_name):
        """Создание ярлыка на рабочем столе"""
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, f"{shortcut_name}.lnk")
            
            # Создаем ярлык через VBS скрипт
            vbs_script = f"""
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{target_path}"
oLink.Save
"""
            
            with open("create_shortcut.vbs", "w") as f:
                f.write(vbs_script)
            
            os.system("create_shortcut.vbs")
            os.remove("create_shortcut.vbs")
            
            return f"✅ Ярлык '{shortcut_name}' создан на рабочем столе"
            
        except Exception as e:
            return f"❌ Ошибка создания ярлыка: {e}"

    def system_cleanup(self):
        """Быстрая очистка временных файлов"""
        try:
            # Очистка временных файлов
            temp_dir = os.environ.get('TEMP', '')
            if temp_dir:
                os.system(f'del /q/f/s "{temp_dir}\\*" >nul 2>&1')
            
            # Очистка корзины
            os.system('powershell -Command "Clear-RecycleBin -Force"')
            
            return "✅ Временные файлы и корзина очищены"
            
        except Exception as e:
            return f"❌ Ошибка очистки: {e}"

# Глобальный экземпляр для использования в других модулях
automation_skills = AutomationSkills()