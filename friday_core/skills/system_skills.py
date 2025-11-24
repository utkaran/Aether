# friday_core/skills/system_skills.py

import os
import subprocess
import platform

class SystemSkills:
    @staticmethod
    def shutdown(seconds=60):
        """Выключение компьютера"""
        try:
            if platform.system() == "Windows":
                os.system(f"shutdown /s /t {seconds}")
                return f"Компьютер будет выключен через {seconds} секунд"
            else:
                # Для Linux/Mac
                os.system(f"shutdown -h +{seconds//60}")
                return f"Компьютер будет выключен через {seconds} секунд"
        except Exception as e:
            return f"Ошибка выключения: {e}"

    @staticmethod
    def restart(seconds=60):
        """Перезагрузка компьютера"""
        try:
            if platform.system() == "Windows":
                os.system(f"shutdown /r /t {seconds}")
                return f"Компьютер будет перезагружен через {seconds} секунд"
            else:
                # Для Linux/Mac
                os.system(f"shutdown -r +{seconds//60}")
                return f"Компьютер будет перезагружен через {seconds} секунд"
        except Exception as e:
            return f"Ошибка перезагрузки: {e}"

    @staticmethod
    def cancel_shutdown():
        """Отмена выключения/перезагрузки"""
        try:
            if platform.system() == "Windows":
                os.system("shutdown /a")
                return "Выключение отменено"
            else:
                # Для Linux/Mac
                os.system("shutdown -c")
                return "Выключение отменено"
        except Exception as e:
            return f"Ошибка отмены выключения: {e}"

    @staticmethod
    def sleep():
        """Перевод компьютера в спящий режим"""
        try:
            if platform.system() == "Windows":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return "Перевод компьютера в спящий режим"
            else:
                # Для Linux
                os.system("systemctl suspend")
                return "Перевод компьютера в спящий режим"
        except Exception as e:
            return f"Ошибка перевода в спящий режим: {e}"

    @staticmethod
    def lock_screen():
        """Блокировка экрана"""
        try:
            if platform.system() == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return "Экран заблокирован"
            else:
                # Для Linux (GNOME)
                os.system("gnome-screensaver-command -l")
                return "Экран заблокирован"
        except Exception as e:
            return f"Ошибка блокировки экрана: {e}"

    @staticmethod
    def get_system_info():
        """Получение информации о системе"""
        try:
            system_info = f"""
Системная информация:
- ОС: {platform.system()} {platform.release()}
- Архитектура: {platform.architecture()[0]}
- Процессор: {platform.processor()}
- Python: {platform.python_version()}
"""
            return system_info
        except Exception as e:
            return f"Ошибка получения информации о системе: {e}"