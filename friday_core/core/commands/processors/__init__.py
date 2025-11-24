from .audio import AudioCommandProcessor
from .system import SystemCommandProcessor
from .weather import WeatherCommandProcessor
from .media import MediaCommandProcessor
from .basic import BasicCommandProcessor
from .config import ConfigCommandProcessor

__all__ = [
    'AudioCommandProcessor',
    'SystemCommandProcessor', 
    'WeatherCommandProcessor',
    'MediaCommandProcessor',
    'BasicCommandProcessor',
    'ConfigCommandProcessor'
]