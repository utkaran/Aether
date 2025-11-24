# friday_core/__init__.py

from friday_core.main import Friday, main
from friday_core.config.config import config
from friday_core.engine.voice_engine import VoiceEngine


__version__ = '1.0.0'
__all__ = ['Friday', 'main', 'config', 'VoiceEngine']