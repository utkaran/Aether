# friday_core/utills/logger.py

import logging
import sys
from pathlib import Path
from datetime import datetime

class PerfomanceLogger:
  def __init__(self):
    Path("logs").mkdir(exist_ok=True)

    self.logger = logging.getLogger("FridayAI")
    self.logger.setLevel(logging.INFO)

    # Файловый handler

    file_handler = logging.FileHandler(
      f'logs/friday_{datetime.now().strftime("%Y%m%d")}.log',
      encoding='utf-8'
    )

    file_handler.setLevel(logging.INFO)

    # Консольный handler

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)

    # Форматтер

    formatter = logging.Formatter(
      '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    self.logger.addHandler(file_handler)
    self.logger.addHandler(console_handler)

    self.command_times = []
    self.error_count = 0


  def log_command(self, command, processing_time, success=True):
    self.command_times.append(processing_time)
    status = 'success' if success else 'failed'
    self.logger.info(f"Command: '{command}' | Time: {processing_time:.2f}s | Status: {status}")

    # Автоочистка старых записей
    if len(self.command_times) > 1000:
      self.command_times = self.command_times[-500:]

  def get_performance_stats(self):
    if not self.command_times:
      return "No commands processed yet"
    
    avg_time = sum(self.command_times) / len(self.command_times)
    max_time = max(self.command_times)
    min_time = min(self.command_times)

    return {
      'total_commands': len(self.command_times),
      'avg_processing_time': avg_time,
      'max_processing_time': max_time,
      'min_processing_time': min_time,
      'error_rate': self.error_count / max(len(self.command_times), 1)
    }
  
perfomance_logger = PerfomanceLogger()