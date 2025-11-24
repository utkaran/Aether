# friday_core/engine/pygame_edge_tts.py

import os
import subprocess
import tempfile
from pygame import mixer
from friday_core.config.config import config

class PygameEdgeTTS:
    def __init__(self):
        print("🔧 Инициализация Pygame Edge-TTS...")
        self.voice = config.get('voice.edge_voice', 'ru-RU-SvetlanaNeural')
        self.rate = config.get('voice.rate', 150)
        
        # Инициализируем pygame mixer
        try:
            mixer.init()
            self.mixer_available = True
            print("✅ Pygame mixer инициализирован")
        except Exception as e:
            self.mixer_available = False
            print(f"❌ Pygame mixer не доступен: {e}")
        
        print(f"✅ Pygame Edge-TTS готов. Голос: {self.voice}")

    def speak(self, text):
        """Озвучка с воспроизведением через pygame"""
        if not text or not text.strip():
            return

        print(f"🔊 Pygame Edge-TTS: '{text}'")
        
        temp_filename = None
        
        try:
            # Создаем временный файл
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                temp_filename = tmp_file.name

            # Преобразуем скорость
            rate_str = self._convert_rate(self.rate)
            
            # Команда для генерации
            cmd = [
                "edge-tts",
                "--text", text,
                "--voice", self.voice,
                "--write-media", temp_filename
            ]
            
            if rate_str != "+0%":
                cmd.extend(["--rate", rate_str])
            
            print(f"🔧 Генерация речи...")
            
            # Генерируем речь
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(temp_filename):
                file_size = os.path.getsize(temp_filename)
                print(f"✅ Речь сгенерирована ({file_size} байт), воспроизвожу...")
                
                # Воспроизводим через pygame
                if self.mixer_available:
                    mixer.music.load(temp_filename)
                    mixer.music.play()
                    
                    # Ждем окончания воспроизведения
                    while mixer.music.get_busy():
                        import time
                        time.sleep(0.1)
                    
                    print("✅ Речь воспроизведена через pygame")
                else:
                    print("❌ Pygame mixer не доступен для воспроизведения")
                
            else:
                print(f"❌ Ошибка генерации: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Ошибка озвучки: {e}")
        finally:
            # Удаляем временный файл
            if temp_filename and os.path.exists(temp_filename):
                try:
                    os.unlink(temp_filename)
                except:
                    pass

    def _convert_rate(self, rate_number):
        """Конвертирует скорость в строковый формат"""
        if rate_number == 150:
            return "+0%"
        elif rate_number <= 50:
            return "-50%"
        elif rate_number >= 300:
            return "+50%"
        else:
            percentage = ((rate_number - 150) / 150) * 50
            percentage = max(-50, min(50, percentage))
            return f"{percentage:+.0f}%"

    def set_voice(self, voice_name):
        self.voice = voice_name
        config.set('voice.edge_voice', voice_name)

    def set_rate(self, rate_number):
        self.rate = rate_number
        config.set('voice.rate', rate_number)