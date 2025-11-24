from typing import List, Optional
from .base import CommandProcessor, CommandContext
import time

class CommandRouter:
  def __init__(self, processors: List[CommandProcessor]):
    self.processors = processors

  def route(self, command: str, user_id: Optional[str]=None) -> str:
    if not command:
      return 'Не услышал вас, сэр'
    
    context = CommandContext (
      original_command = command,
      user_id = user_id,
      timestamp = time.time()
    )

    for processor in self.processors:
      if processor.can_handle(command):
        try:
          result = processor.process(command, context)
          print(f'Обработано {processor.__class__.__name__}: {result}')
          return result
        
        except Exception as e:
          print(f'Ошибка в {processor.__class__.__name__}: {e}')
          return f'Ошибка обработки команды: {e}'
        

    return 'Извините, я не понял команды. Скажите "помощь" для списка команд'