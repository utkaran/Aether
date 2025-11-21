# launch_gui.py

import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
  try:
    from friday_core.gui.simple_interface import FridayGUI
    print("Запуск Пятницы с графическим интерфейсом...")
    gui = FridayGUI()
    gui.run()

  except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("🔧 Убедитесь, что все зависимости установлены")
    input("Нажмите Enter для выхода...")

  except Exception as e:
    print(f"💥 Критическая ошибка: {e}")
    input("Нажмите Enter для выхода...")

if __name__ == '__main__':
  main()