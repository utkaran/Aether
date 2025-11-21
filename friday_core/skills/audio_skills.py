# Регулировка громкости

import os
import subprocess

class AudioSkills:
    @staticmethod
    def set_volume(level):
        """Установка громкости через svcl"""
        try:
            if not os.path.exists("svcl.exe"):
                return "Утилита регулировки громкости не найдена"
            
            level = max(0, min(100, int(level)))
            subprocess.run(['svcl.exe', '/SetVolume', '0', str(level)], 
                         timeout=10, check=True, capture_output=True)
            return f"Громкость установлена на {level}%"
        except subprocess.TimeoutExpired:
            return "Таймаут при установке громкости"
        except subprocess.CalledProcessError:
            return "Ошибка выполнения команды громкости"
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def volume_up():
        """Увеличить громкость на 20%"""
        try:
            if not os.path.exists("svcl.exe"):
                return "Утилита регулировки громкости не найдена"
            
            subprocess.run(['svcl.exe', '/ChangeVolume', '0', '+20'], 
                         timeout=10, check=True, capture_output=True)
            return "Громкость увеличена"
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def volume_down():
        """Уменьшить громкость на 20%"""
        try:
            if not os.path.exists("svcl.exe"):
                return "Утилита регулировки громкости не найдена"
            
            subprocess.run(['svcl.exe', '/ChangeVolume', '0', '-20'], 
                         timeout=10, check=True, capture_output=True)
            return "Громкость уменьшена"
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def mute():
        """ВЫКЛЮЧИТЬ ЗВУК (громкость на 1%)"""
        try:
            if not os.path.exists("svcl.exe"):
                return "Утилита регулировки громкости не найдена"
            
            subprocess.run(['svcl.exe', '/SetVolume', '0', '1'], 
                         timeout=10, check=True, capture_output=True)
            return "Звук выключен"
        except Exception as e:
            return f"Ошибка выключения звука: {e}"

    @staticmethod
    def unmute():
        """ВКЛЮЧИТЬ ЗВУК (громкость на 50%)"""
        try:
            if not os.path.exists("svcl.exe"):
                return "Утилита регулировки громкости не найдена"
            
            subprocess.run(['svcl.exe', '/SetVolume', '0', '50'], 
                         timeout=10, check=True, capture_output=True)
            return "Звук включен на 50%"
        except Exception as e:
            return f"Ошибка включения звука: {e}"