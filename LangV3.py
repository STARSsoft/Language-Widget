from pynput import keyboard
import tkinter as tk
import threading

current_keys = set()

lang_map = {
    'ru': 'RUS',
    'kz': 'KAZ',
    'us': 'ENG'
}

current_lang = 'us'
lang_cycle = iter(lang_map.keys())
popup_counter = 0  # Счетчик для уникальных имен окон
popup_position = (20, 20)  # Начальная позиция окна

def switch_language():
    global current_lang, lang_cycle
    try:
        current_lang = next(lang_cycle)
    except StopIteration:
        lang_cycle = iter(lang_map.keys())
        current_lang = next(lang_cycle)

def show_popup():
    global popup_counter, popup_position
    popup_counter += 1
    popup = tk.Tk()
    popup.geometry(f"100x50+{popup_position[0]}+{popup_position[1]}")  # Ширина, высота, отступ слева, отступ сверху
    popup.title(f"Language_{popup_counter}")
    label = tk.Label(popup, text=lang_map[current_lang], font=("Arial Bold", 30))
    label.pack()
    popup.after(3000, lambda: popup.destroy())  # Закрыть окно через 3 секунды
    #popup_position = (popup_position[0] + 30, popup_position[1] + 30)  # Смещение следующего окна
    popup.mainloop()

def show_popup_thread():
    popup_thread = threading.Thread(target=show_popup)
    popup_thread.start()

def on_press(key):
    global current_lang, lang_cycle
    try:
        if key == keyboard.Key.alt_l:
            current_keys.add('alt')
        elif key == keyboard.Key.shift:
            current_keys.add('shift')
        elif key == keyboard.Key.cmd:
            current_keys.add('super')
        elif key == keyboard.Key.space:
            current_keys.add('space')
        
        # Проверка комбинации Alt + Shift
        if 'alt' in current_keys and 'shift' in current_keys:
            print("Вы нажали Alt + Shift")
            switch_language()
            print(f"Текущий язык: {lang_map[current_lang]}")
            show_popup_thread()
            
        # Проверка комбинации Super + Space
        if 'super' in current_keys and 'space' in current_keys:
            print("Вы нажали Super + Space")
            switch_language()
            print(f"Текущий язык: {lang_map[current_lang]}")
            show_popup_thread()
    except AttributeError:
        pass

def on_release(key):
    try:
        if key == keyboard.Key.alt_l:
            current_keys.discard('alt')
        elif key == keyboard.Key.shift:
            current_keys.discard('shift')
        elif key == keyboard.Key.cmd:
            current_keys.discard('super')
        elif key == keyboard.Key.space:
            current_keys.discard('space')
    except AttributeError:
        pass

    if key == keyboard.Key.esc:
        # Остановить прослушивание при нажатии клавиши ESC
        return False

# Запуск прослушивания клавиатуры
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
