# base_neuron.py

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from friday_core.utills.event_bus import event_bus, EventType

class BaseNeuron(ABC):
  def __init__(self, name:str):
    self.name = name
    self.is_active = True
    self.error_count = 0
    self.max_errors = 3
    print(f"Нейрон '{name}' инициализирован")

  @abstractmethod
  # Может ли нейрон обработать команду
  def can_handle(self, command:str) -> bool:
    pass

  @abstractmethod
  # Обработка команды
  def process(self, command: str) -> str:
    pass

  def handle_safely(self, command:str) -> Optional[str]:
    # Безопасная обработка с изоляцией ошибок

    if not self.is_active:
      return None
    
    try:
      if self.can_handle(command):
        print(f'Нейрон "{self.name}" обрабатывает: "{command}"')
        result = self.process(command)
        self.error_count = 0
        event_bus.publish(EventType.COMMAND_EXECUTED, {
          'neuron': self.name,
          'command': command,
          'success': True
        })

        return result
      
    except Exception as e:
      self.error_count += 1
      print(f'Нейрон "{self.name}" не работает. Ошибка: {e}')

      if self.error_count >= self.max_errors:
        self.is_active = False
        print(f'Нейрон "{self.name}" отключен из за ошибок')

      event_bus.publish(EventType.ERROR_OCCURRED, {
        'neuron': self.name,
        'error': str(e),
        'command': command
      })

    return None
  
  def __repr__(self):
    return f'Нейрон("{self.name}", acrtive={self.is_active}, errors={self.error_count})'
