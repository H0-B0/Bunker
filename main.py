import tkinter as tk
import os
import sys
import shutil
import traceback
from sozdat import sozdat
from connect import connect
from rules import rules

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_app_data_path():
    if hasattr(sys, '_MEIPASS'):
        if sys.platform.startswith('win'):
            app_data_path = os.path.join(os.environ['LOCALAPPDATA'], 'BunkerGame')
        else:
            home = os.path.expanduser("~")
            app_data_path = os.path.join(home, '.local', 'share', 'BunkerGame')
    else:
        app_data_path = os.path.join(os.path.abspath("."), 'BunkerGame_Data')
    os.makedirs(app_data_path, exist_ok=True)
    return app_data_path

def setup_resources():
    app_data_path = get_app_data_path()
    resource_path = get_resource_path('.')
    resource_files = os.listdir(resource_path)
    db_files = [f for f in resource_files if f.endswith('.db')]
    if not db_files:
        raise Exception("Не найдена БД в ресурсах exe!")
    DB_NAME = db_files[0]
    icon_ico_path = os.path.join(app_data_path, 'bunker.ico')
    icon_png_path = os.path.join(app_data_path, 'bunker.png')
    db_path = os.path.join(app_data_path, DB_NAME)

    source_db = get_resource_path(DB_NAME)
    shutil.copy2(source_db, db_path)
    print(f"БД скопирована: {DB_NAME} -> {db_path}")

    if not os.path.exists(icon_png_path):
        source_png = get_resource_path('bunker.png')
        if os.path.exists(source_png):
            shutil.copy2(source_png, icon_png_path)
            print("PNG иконка скопирована")
    if not os.path.exists(icon_ico_path):
        source_ico = get_resource_path('bunker.ico')
        if os.path.exists(source_ico):
            shutil.copy2(source_ico, icon_ico_path)
            print("ICO иконка скопирована")
    return icon_png_path, icon_ico_path, db_path

# Получение путей
ICON_PNG_PATH, ICON_ICO_PATH, DB_PATH = setup_resources()
print(f"DB_PATH: {DB_PATH}, exists={os.path.exists(DB_PATH)}")

def made():
    okno.destroy()
    sozdat(ICON_PNG_PATH, ICON_ICO_PATH, DB_PATH)


def prisoedinitsa():
    okno.destroy()
    connect(ICON_PNG_PATH, ICON_ICO_PATH, DB_PATH)

def book():
    okno.destroy()
    rules(ICON_PNG_PATH, ICON_ICO_PATH, DB_PATH)

# ========== ГЛАВНОЕ ОКНО ==========
okno = tk.Tk()
okno.title("Бункер")
okno.geometry('1200x1000')
if sys.platform.startswith('win'):
    okno.state('zoomed')
else:
    try:
        okno.attributes('-zoomed', True)
    except:
        okno.state('normal')

BG_COLOR = "#1A1A1A"
TEXT_COLOR = "#E0E0E0"
ACCENT_COLOR = "#FF7B30"
BUTTON_BG = "#2D2D2D"
BUTTON_ACTIVE = "#CC5500"

okno.configure(bg=BG_COLOR)

# Установка иконки
if sys.platform.startswith('win') and os.path.exists(ICON_ICO_PATH):
    okno.iconbitmap(ICON_ICO_PATH)
elif os.path.exists(ICON_PNG_PATH):
    try:
        img = tk.PhotoImage(file=ICON_PNG_PATH)
        okno.iconphoto(True, img)
    except:
        pass

# Стили
TITLE_STYLE = {"font": ("Courier New", 24, "bold"), "bg": BG_COLOR, "fg": ACCENT_COLOR}
ZAGOLOVOK_STYLE = {"font": ("Arial", 14, "bold"), "bg": BG_COLOR}
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

title_label = tk.Label(okno, text="🚧 БУНКЕР 🚧", **TITLE_STYLE)
title_label.pack(pady=(50, 30))

label1 = tk.Label(okno, text="Создать комнату", **ZAGOLOVOK_STYLE, fg=TEXT_COLOR)
label1.pack(pady=(20, 10))
soz = tk.Button(okno, text="🔨", command=made, **BUTTON_STYLE)
soz.pack(pady=10)

separator = tk.Frame(okno, height=2, bg=ACCENT_COLOR)
separator.pack(fill="x", padx=100, pady=30)

label2 = tk.Label(okno, text="Присоединиться к комнате", **ZAGOLOVOK_STYLE, fg=TEXT_COLOR)
label2.pack(pady=(20, 10))
con = tk.Button(okno, text="🔗", command=prisoedinitsa, **BUTTON_STYLE)
con.pack(pady=10)

separator = tk.Frame(okno, height=2, bg=ACCENT_COLOR)
separator.pack(fill="x", padx=100, pady=30)

label3 = tk.Label(okno, text="Правила игры", **ZAGOLOVOK_STYLE, fg=TEXT_COLOR)
label3.pack(pady=(20, 10))
pravila = tk.Button(okno, text="📜", command=book, **BUTTON_STYLE)
pravila.pack(pady=10)

footer = tk.Label(okno, text="⚡ Выживайте любой ценой ⚡",
                 font=("Arial", 10, "italic"), bg=BG_COLOR, fg=TEXT_COLOR)
footer.pack(side="bottom", pady=20)

okno.mainloop()