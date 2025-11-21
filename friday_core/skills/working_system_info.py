import platform
import datetime
import os

class WorkingSystemInfo:
    @staticmethod
    def get_info():
        """ГАРАНТИРОВАННО РАБОЧАЯ информация о системе"""
        try:
            info = f"""
ИНФОРМАЦИЯ О СИСТЕМЕ:

  Операционная система: {platform.system()} {platform.release()}
 Архитектура: {platform.architecture()[0]}
 Python: {platform.python_version()}
 Текущее время: {datetime.datetime.now().strftime('%H:%M:%S')}
 Дата: {datetime.datetime.now().strftime('%d.%m.%Y')}
 Рабочая папка: {os.getcwd()}
"""
            # Дополнительно для Windows
            if platform.system() == "Windows":
                computer_name = os.getenv('COMPUTERNAME', 'не определен')
                username = os.getenv('USERNAME', 'не определен')
                info += f" Имя ПК: {computer_name}\n"
                info += f" Пользователь: {username}\n"
            
            return info
            
        except Exception as e:
            return f"❌ Ошибка получения информации: {e}"

# Тест класса
'''if __name__ == "__main__":
    print("🧪 ТЕСТ WorkingSystemInfo:")
    print(WorkingSystemInfo().get_info())'''