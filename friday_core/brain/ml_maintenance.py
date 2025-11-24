# friday_core/brain/ml_maintenance.py

import json
import os
import time
from datetime import datetime

class MLMaintenance:
  def __init__(self, intent_classifier):
    self.intent_classifier = intent_classifier
    self.commands_since_last_training = 0
    self.max_commands_before_retrain = 100
    self.max_interaction_logs = 1000
    self.max_command_sequences = 500
    self.commands_per_cleanup = 50

    print("Инициализирован менеджер обслуживания ML")

  def record_command(self):
    self.commands_since_last_training += 1

    if self.commands_since_last_training >= self.max_commands_before_retrain:
      self.retrain_model()
        
    if self.commands_since_last_training % self.commands_per_cleanup == 0:
      self.cleanup_all_logs()

  def retrain_model(self):
    try:
        print("🔄 Автоматическое переобучение ML модели...")
        accuracy = self.intent_classifier.train()
        self.commands_since_last_training = 0
            
            # Логируем переобучение
        self._log_training(accuracy)
        print(f"✅ Модель переобучена! Точность: {accuracy:.2f}")
            
        return accuracy
    except Exception as e:
      print(f"❌ Ошибка переобучения модели: {e}")
      return 0
    
  def cleanup_all_logs(self):
    try:
      cleaned_files = []

      if self._cleanup_interaction_logs():
        cleaned_files.append('логи взаимодействий')
      if self._cleanup_reccomendation_logs():
        cleaned_files.append('логи рекомендаций')
      if self._cleanup_temp_files():
        cleaned_files.append('временные файлы')

      if cleaned_files:
        print(f"Очищены: {', '.join(cleaned_files)}")
      else:
        print('Логи уже чистые')

    except Exception as e:
      print(f'Ошибка очистки логов: {e}')
  
  def _cleanup_interaction_logs(self):
    try:
      log_file = 'ml_models/interaction_log.jsonl'
      if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
          lines = f.readlines()

        if len(lines) > self.max_interaction_logs:
          keep_lines = lines[-self.max_interaction_logs:]

          with open(log_file, 'w', encoding='utf-8') as f:
            f.writelines(keep_lines)

          return True
        
      return False
    
    except Exception as e:
      print(f'Ошибка очистки логов: {e}')
      return False
    
  def _cleanup_reccomendation_logs(self):
    try:
      habbits_file = "ml_models/user_habits.json"
      if os.path.exists(habbits_file):
        with open(habbits_file, 'r', encoding='utf-8') as f:
          habbits = json.load(f)

        cleaned = False

        if 'command_sequences' in habbits and len(habbits['command_sequences']) > self.max_command_sequences:
          habbits['command_sequences'] = habbits['command_sequences'][-self.max_command_sequences:]
          cleaned = True

        if 'time_based_commands' in habbits:
          for time_slot in ['morning', 'afternoon', 'evening', 'night']:
            if time_slot in habbits['time_based_commands']:
              time_commands = habbits['time_based_commands'][time_slot]
              if isinstance(time_commands, dict) and len(time_commands) > 20:
                top_commands = dict(sorted(time_commands.items(), key=lambda x: x[1], reverse=True)[:20])
                habbits['time_based_commands'][time_slot] = top_commands
                cleaned = True

        if cleaned:
          with open(habbits_file, 'w', encoding='utf-8') as f:
            json.dump(habbits, f, ensure_ascii=False, indent=2)

        return cleaned
      return False
    except Exception as e:
      print(f'Ошибка очистки логов рекомендаций: {e}')
      return False
    
  def _cleanup_temp_files(self):
    try:
      temp_files = [
      "ml_models/temp_training_data.pkl",
      "ml_models/vectorizer_cache.pkl"
      ]

      cleaned = False

      for temp_file in temp_files:
        if os.path.exists(temp_file):
          os.remove(temp_file)
          cleaned = True

      return cleaned
    except Exception as e:
      print(f'Ошибка очистки временных файлов: {e}')
      return False
    
  def _log_training(self, accuracy):
    try:
      log_entry = {
        'type': 'automatic_retraining',
        'timestamp': datetime.now().isoformat(),
        'commands_processed': self.max_commands_before_retrain,
        'accuracy': accuracy,
        'training_size': len(self.intent_classifier.prepare_training_data()[0])
      }

      os.makedirs('ml_models', exist_ok=True)
      log_file = 'ml_models/training_history.jsonl'

      with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False)+ '\n')

      print(f'Логирование обучения: accuracy={accuracy:.2f}')
    except Exception as e:
      print(f'Ошибка логирования обучения: {e}')

  def get_status(self):
    remaining = max(0, self.max_commands_before_retrain - self.commands_since_last_training)
    return {
      'commands_since_training': self.commands_since_last_training,
      'commands_until_retrain': remaining,
      'max_logs': self.max_interaction_logs,
      'max_sequences': self.max_command_sequences
    }
  
  def manual_cleanup(self):
    print('Очистка логов.......')
    self.cleanup_all_logs()
    return 'Проведена ручная очистка логов ML модели'
  
  def manual_retrain(self):
    print('Ручное переобучение модели....')
    accuracy = self.retrain_model()
    return f'Модель переобучена вручную. Точность: {accuracy:.2f}'
  
    

