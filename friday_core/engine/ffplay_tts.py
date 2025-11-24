# friday_core/engine/ffplay_tts.py

import os
import subprocess
import tempfile
import time
from friday_core.config.config import config

class FFplayTTS:
    def __init__(self):
        print("🔧 Инициализация FFplay TTS...")
        
        # ПРЯМАЯ загрузка из конфига
        from friday_core.config.config import config
        self.voice = config.get('voice.edge_voice', 'ru-RU-SvetlanaNeural')
        self.rate = config.get('voice.rate', 150)
        
        print(f"✅ FFplay TTS готов. Голос: {self.voice}, Скорость: {self.rate}")

    def get_available_voices(self):
        try:
            print("🔍 Получение списка голосов...")
            
            # Запускаем команду для получения списка голосов
            cmd = ["edge-tts", "--list-voices"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                voices = []
                lines = result.stdout.split('\n')
                
                for line in lines:
                    if 'ru-' in line.lower() and 'Name:' in line:
                        # Извлекаем информацию о голосе
                        parts = line.split('Name: ')
                        if len(parts) > 1:
                            voice_info = parts[1].strip()
                            # Ищем короткое имя голоса
                            if 'ShortName:' in voice_info:
                                short_parts = voice_info.split('ShortName: ')
                                if len(short_parts) > 1:
                                    voice_name = short_parts[1].split()[0]
                                    voices.append(voice_name)
                
                print(f"✅ Найдено {len(voices)} русских голосов")
                return voices
            else:
                print(f"❌ Ошибка получения голосов: {result.stderr}")
                return []
                
        except subprocess.TimeoutExpired:
            print("❌ Таймаут при получении голосов")
            return []
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return []

    def speak(self, text):
        """Быстрая озвучка через FFplay"""
        if not text or not text.strip():
            return

        print(f"🔊 FFplay TTS: '{text}'")
        
        temp_filename = None
        
        try:
            # Создаем временный файл
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                temp_filename = tmp_file.name

            # Генерируем речь
            rate_str = self._convert_rate(self.rate)
            cmd_gen = [
                "edge-tts",
                "--text", text,
                "--voice", self.voice,
                "--write-media", temp_filename
            ]
            
            if rate_str != "+0%":
                cmd_gen.extend(["--rate", rate_str])

            print("🔧 Генерация...")
            result_gen = subprocess.run(cmd_gen, capture_output=True, timeout=30)
            
            if result_gen.returncode != 0:
                print(f"❌ Ошибка генерации: {result_gen.stderr}")
                return

            # Проверяем файл
            if not os.path.exists(temp_filename):
                print("❌ Файл не создан")
                return
                
            file_size = os.path.getsize(temp_filename)
            if file_size < 1000:
                print("❌ Файл слишком маленький")
                return

            print(f"✅ Файл готов ({file_size} байт), воспроизведение...")
            
            # Воспроизводим через FFplay
            cmd_play = [
                "ffplay",
                "-autoexit",    # Автоматически выходит после воспроизведения
                "-nodisp",      # Не показывает окно
                "-loglevel", "quiet",  # Тихий режим
                temp_filename
            ]
            
            subprocess.run(cmd_play, timeout=30)
            print("✅ Речь воспроизведена!")
            
        except subprocess.TimeoutExpired:
            print("❌ Таймаут")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        finally:
            # Очистка
            if temp_filename and os.path.exists(temp_filename):
                try:
                    os.unlink(temp_filename)
                except:
                    pass

    def _convert_rate(self, rate_number):
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
        print(f"Устанавливаю голос: {voice_name}")
        self.voice = voice_name
        config.set('voice.edge_voice', voice_name)
        print(f'Голос установлен: {config.get("voice.edge_voice")}')

    def set_rate(self, rate_number):
        self.rate = rate_number
        config.set('voice.rate', rate_number)
        print(f"Скорость установлена: {rate_number}")