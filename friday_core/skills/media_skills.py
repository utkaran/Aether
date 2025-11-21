import os
import webbrowser

class MediaKills:
  @staticmethod
  def play_music():
    webbrowser.open("https://www.youtube.com")
    return 'Включаю музыку'
  
  @staticmethod
  def play_on_youtube(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    return f'Ищу на Youtube: {query}'
  
  @staticmethod
  def play_hitmo():
    webbrowser.open('https://rus.hitmotop.com/')
    return 'Открываю hitmo'
  
  @staticmethod
  def pause_media():
    try:
      from pynput.keyboard import Key, Controller
      keyboard = Controller()
      keyboard.press(Key.media_play_pause)
      keyboard.release(Key.media_play_pause)
      return 'Пауза'
    except:
      return 'Не удалось поставить на паузу'