# friday_core/engine/pygame_edge_tts.py

import pygame
import numpy
import math
import time
from friday_core.config.config import config

class SoundManager:
    def __init__(self):
        print("🔊 Инициализация менеджера звуков Pygame...")
        self.sound_enabled = True
        
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            self.pygame_available = True
            print("✅ Pygame звуковая система готова")
        except Exception as e:
            self.pygame_available = False
            print(f"❌ Ошибка инициализации Pygame: {e}")
    
    def _is_sound_enabled(self):
        """Проверяет, включены ли звуки в конфигурации"""
        return config.get('sounds.enabled', True) and self.sound_enabled
    
    def apply_envelope(self, samples, sample_rate, attack=0.1, decay=0.1, sustain=0.7, release=0.2):
        """Применяет ADSR-огибающую для плавного звука"""
        total_samples = len(samples)
        attack_samples = int(attack * total_samples)
        decay_samples = int(decay * total_samples)
        release_samples = int(release * total_samples)
        sustain_samples = total_samples - attack_samples - decay_samples - release_samples
        
        envelope = numpy.zeros(total_samples)
        
        # Attack (плавное нарастание)
        for i in range(attack_samples):
            envelope[i] = i / attack_samples
        
        # Decay (плавный спад до уровня sustain)
        for i in range(decay_samples):
            envelope[attack_samples + i] = 1.0 - (1.0 - sustain) * (i / decay_samples)
        
        # Sustain (удержание)
        for i in range(sustain_samples):
            envelope[attack_samples + decay_samples + i] = sustain
        
        # Release (плавное затухание)
        for i in range(release_samples):
            envelope[attack_samples + decay_samples + sustain_samples + i] = sustain * (1.0 - i / release_samples)
        
        return samples * envelope
    
    def generate_smooth_tone(self, frequency=440, duration=500, volume=0.5, wave_type='sine'):
        """Генерирует плавный тон с огибающей"""
        if not self.pygame_available or not self._is_sound_enabled():
            return None
            
        try:
            sample_rate = 44100
            n_samples = int(round(duration * 0.001 * sample_rate))
            
            # Создаем основной тон
            samples = numpy.zeros(n_samples)
            max_sample = 2**(16 - 1) - 1
            
            for i in range(n_samples):
                t = float(i) / sample_rate
                
                if wave_type == 'sine':
                    sample = math.sin(2 * math.pi * frequency * t)
                elif wave_type == 'triangle':
                    # Треугольная волна - мягче чем пила
                    sample = 2.0 * abs(2.0 * (t * frequency - math.floor(t * frequency + 0.5))) - 1.0
                else:
                    sample = math.sin(2 * math.pi * frequency * t)
                
                samples[i] = sample
            
            # Применяем огибающую для плавности
            samples = self.apply_envelope(samples, sample_rate, 
                                        attack=0.1, decay=0.2, sustain=0.6, release=0.3)
            
            # Конвертируем в стерео
            buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)
            for i in range(n_samples):
                sample_value = max_sample * volume * samples[i]
                buf[i][0] = int(round(sample_value))
                buf[i][1] = int(round(sample_value))
                
            return pygame.sndarray.make_sound(buf)
            
        except Exception as e:
            print(f"❌ Ошибка генерации плавного звука: {e}")
            return None
    
    def play_activation(self):
        """Плавный звук активации"""
        if not self._is_sound_enabled() or not self.pygame_available:
            return
            
        print("🔊 Звук активации Пятницы")
        try:
            # Восходящая последовательность с плавными переходами
            sound1 = self.generate_smooth_tone(400, 200, 0.4, 'sine')
            sound2 = self.generate_smooth_tone(600, 250, 0.3, 'sine')
            sound3 = self.generate_smooth_tone(800, 300, 0.2, 'sine')
            
            if sound1 and sound2 and sound3:
                sound1.play()
                pygame.time.wait(220)  # Ждем почти полной длительности
                sound2.play()
                pygame.time.wait(270)
                sound3.play()
        except Exception as e:
            print(f"❌ Ошибка звука активации: {e}")
    
    def play_success(self):
        """Плавный звук успеха"""
        if not self._is_sound_enabled() or not self.pygame_available:
            return
            
        print("🔊 Звук успеха")
        try:
            # Два плавных тона с небольшой паузой
            sound = self.generate_smooth_tone(1000, 400, 0.3, 'sine')
            if sound:
                sound.play()
        except Exception as e:
            print(f"❌ Ошибка звука успеха: {e}")
    
    def play_error(self):
        """Плавный звук ошибки"""
        if not self._is_sound_enabled() or not self.pygame_available:
            return
            
        print("🔊 Звук ошибки")
        try:
            # Низкий плавный тон
            sound = self.generate_smooth_tone(300, 500, 0.4, 'triangle')
            if sound:
                sound.play()
        except Exception as e:
            print(f"❌ Ошибка звука ошибки: {e}")
    
    def play_listening(self):
        """Короткий плавный звук"""
        if not self._is_sound_enabled() or not self.pygame_available:
            return
            
        print("🔊 Звук прослушивания")
        try:
            sound = self.generate_smooth_tone(700, 200, 0.2, 'sine')
            if sound:
                sound.play()
        except Exception as e:
            print(f"❌ Ошибка звука прослушивания: {e}")
    
    def play_notification(self):
        """Плавный звук уведомления"""
        if not self._is_sound_enabled() or not self.pygame_available:
            return
            
        print("🔊 Звук уведомления")
        try:
            sound = self.generate_smooth_tone(800, 300, 0.25, 'sine')
            if sound:
                sound.play()
        except Exception as e:
            print(f"❌ Ошибка звука уведомления: {e}")
    
    def play_startup(self):
        """Плавная последовательность запуска"""
        if not self._is_sound_enabled() or not self.pygame_available:
            return
            
        print("🔊 Звук запуска системы")
        try:
            tones = [
                (300, 300, 0.3),
                (500, 300, 0.3), 
                (700, 400, 0.3)
            ]
            
            for freq, duration, volume in tones:
                sound = self.generate_smooth_tone(freq, duration, volume, 'sine')
                if sound:
                    sound.play()
                    pygame.time.wait(duration + 50)  # Плавные паузы
        except Exception as e:
            print(f"❌ Ошибка звука запуска: {e}")
    
    def play_shutdown(self):
        """Плавная последовательность выключения"""
        if not self._is_sound_enabled() or not self.pygame_available:
            return
            
        print("🔊 Звук выключения системы")
        try:
            tones = [
                (700, 300, 0.3),
                (500, 300, 0.3),
                (300, 400, 0.3)
            ]
            
            for freq, duration, volume in tones:
                sound = self.generate_smooth_tone(freq, duration, volume, 'sine')
                if sound:
                    sound.play()
                    pygame.time.wait(duration + 50)
        except Exception as e:
            print(f"❌ Ошибка звука выключения: {e}")
    
    def set_volume(self, enabled=True):
        """Включить/выключить звуки"""
        self.sound_enabled = enabled
        status = "включены" if enabled else "выключены"
        print(f"🔊 Звуки {status}")

    def play_session_end(self):
        if not self._is_sound_enabled() or not self.pygame_available:
            return
        
        print('Завершение сессии')
        try:
            sound = self.generate_smooth_tone(500, 300, 0.1, 'sine')
            if sound:
                sound.play()
        except Exception as e:
            print('Ошибка звука завершения сессии')

# Глобальный экземпляр
sound_manager = SoundManager()