import tkinter as tk
from sozdat import sozdat
from connect import connect
from rules import rules
import os
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def podmaini(icon_png, icon_ico, db_path):
    
    def made():
        okno.destroy()
        sozdat(icon_png, icon_ico, db_path)

    def prisoedinitsa():
        okno.destroy()
        connect(icon_png, icon_ico, db_path)

    def book():
        okno.destroy()
        rules(icon_png, icon_ico, db_path)

    okno = tk.Tk()
    okno.geometry('1200x1000')
    okno.title("Бункер")
    if sys.platform.startswith('win'):
        okno.state('zoomed')
    else:
        try:
            okno.attributes('-zoomed', True)
        except:
            okno.state('normal')

    # Стиль апокалипсиса (как в main)
    BG_COLOR = "#1A1A1A"  # Тёмно-серый, почти чёрный
    TEXT_COLOR = "#E0E0E0"  # Светло-серый
    ACCENT_COLOR = "#FF7B30"  # Ржавый оранжевый
    BUTTON_BG = "#2D2D2D"  # Тёмно-серый для кнопок
    BUTTON_ACTIVE = "#CC5500"  # Тёмно-оранжевый при нажатии

    okno.configure(bg=BG_COLOR)
    
    if sys.platform.startswith('win'):
        if icon_ico and os.path.exists(icon_ico):
            okno.iconbitmap(icon_ico)
    else:
        try:
            img = tk.PhotoImage(file=icon_png)
            okno.iconphoto(True, img)
        except: pass

    # Стили
    TITLE_STYLE = {"font": ("Courier New", 24, "bold"), "bg": BG_COLOR, "fg": ACCENT_COLOR}
    ZAGOLOVOK_STYLE = {"font": ("Arial", 14, "bold"), "bg": BG_COLOR, "fg": TEXT_COLOR}
    BUTTON_STYLE = {
        "font": ("Arial", 25),
        "width": 3,
        "height": 1,
        "anchor": "center",
        "bg": BUTTON_BG,
        "fg": ACCENT_COLOR,
        "activebackground": BUTTON_ACTIVE,
        "activeforeground": TEXT_COLOR,
        "relief": "raised",
        "bd": 3
    }

    # Заголовок игры
    title_label = tk.Label(okno, text="🚧 БУНКЕР 🚧", **TITLE_STYLE)
    title_label.pack(pady=(50, 30))

    # Создание комнаты
    label1 = tk.Label(okno, text="Создать комнату", **ZAGOLOVOK_STYLE)
    label1.pack(pady=(20, 10))

    soz = tk.Button(okno, text="     🛠️", command=made, **BUTTON_STYLE)
    soz.pack(pady=10)

    # Разделитель
    separator = tk.Frame(okno, height=2, bg=ACCENT_COLOR)
    separator.pack(fill="x", padx=100, pady=30)

    # Присоединение к комнате
    label2 = tk.Label(okno, text="Присоединиться к комнате", **ZAGOLOVOK_STYLE)
    label2.pack(pady=(20, 10))

    con = tk.Button(okno, text="🔗", command=prisoedinitsa, **BUTTON_STYLE)
    con.pack(pady=10)

    # Разделитель
    separator = tk.Frame(okno, height=2, bg=ACCENT_COLOR)
    separator.pack(fill="x", padx=100, pady=30)

    label3 = tk.Label(okno, text="Правила игры", **ZAGOLOVOK_STYLE)
    label3.pack(pady=(20, 10))

    pravila = tk.Button(okno, text="📜", command=book, **BUTTON_STYLE)
    pravila.pack(pady=20)

    # Нижний колонтитул
    footer = tk.Label(okno, text="⚡ Выживайте любой ценой ⚡", 
                     font=("Arial", 10, "italic"), bg=BG_COLOR, fg=TEXT_COLOR)
    footer.pack(side="bottom", pady=20)

    okno.mainloop()

if __name__ == '__main__':
    podmaini()