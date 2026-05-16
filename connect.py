import sqlite3 as sq
import tkinter as tk
from tkinter import ttk
from okno4 import okno4
from okno5 import okno5
from okno6 import okno6
from okno7 import okno7
from okno8 import okno8
from okno9 import okno9
from okno10 import okno10
import os
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def connect(icon_png, icon_ico, db_path):
    
    print(f"connect: db_path = {db_path}")
    print(f"connect: db exists = {os.path.exists(db_path) if db_path else False}")
    
    maximum = 1
    game_code = ''
    player = 1
    server_ip = "127.0.0.1:8000"
    
    def update_label1(event=None):
        nonlocal player
        value = slider1.get()
        value1 = int(value)
        label1.config(text=f"🧍 Ваш номер: {value1}")
        player = value1

    def update_maximum_from_db(event=None):
        nonlocal maximum, game_code
        code = enter.get().strip().upper()
        
        if code and len(code) >= 2:
            try:
                with sq.connect(db_path) as dannie:
                    cur = dannie.cursor()
                    cur.execute("SELECT max_players FROM rooms WHERE code = ?", (code,))
                    data = cur.fetchone()
                    
                    if data:
                        new_maximum = data[0]
                        if new_maximum != maximum:
                            maximum = new_maximum
                            slider1.config(to=maximum)
                            if slider1.get() > maximum:
                                slider1.set(maximum)
                                update_label1()
                            max_label.config(text=f"⚡ Вместимость бункера: {maximum}", fg="#00FF00")
                            status_label.config(text="✅ Бункер обнаружен", fg="#00FF00")
                    else:
                        max_label.config(text="❌ Бункер не найден", fg="#FF0000")
                        status_label.config(text="⚠️ Проверьте код доступа", fg="#FF7B30")
            except sq.Error as e:
                max_label.config(text=f"💀 Ошибка системы: {e}", fg="#FF0000")
                status_label.config(text="⚡ Критический сбой", fg="#FF0000")
        else:
            maximum = 0
            slider1.config(to=maximum)
            if slider1.get() > maximum:
                slider1.set(maximum)
                update_label1()
            max_label.config(text="⚡ Вместимость бункера: 0", fg="#A0A0A0")
            status_label.config(text="⏳ Ожидание кода...", fg="#A0A0A0")
        game_code = enter.get()

    def connection():
        nonlocal maximum, game_code, player, server_ip
        server_ip = ip_entry.get().strip()
        if not server_ip:
            server_ip = '127.0.0.1:8000'
        okno.destroy()
        if maximum == 4:
            okno4(player, game_code, icon_png, icon_ico, db_path, server_ip)
        elif maximum == 5:
            okno5(player, game_code, icon_png, icon_ico, db_path, server_ip)
        elif maximum == 6:
            okno6(player, game_code, icon_png, icon_ico, db_path, server_ip)
        elif maximum == 7:
            okno7(player, game_code, icon_png, icon_ico, db_path, server_ip)
        elif maximum == 8:
            okno8(player, game_code, icon_png, icon_ico, db_path, server_ip)
        elif maximum == 9:
            okno9(player, game_code, icon_png, icon_ico, db_path, server_ip)
        elif maximum == 10:
            okno10(player, game_code, icon_png, icon_ico, db_path, server_ip)

    def back_window():
        okno.destroy()
        import podmain
        podmain.podmaini(icon_png, icon_ico, db_path)

    okno = tk.Tk()
    okno.geometry('1200x1000')
    okno.title('Бункер')
    if sys.platform.startswith('win'):
        okno.state('zoomed')
    else:
        try:
            okno.attributes('-zoomed', True)
        except:
            okno.state('normal')

    # Стиль апокалипсиса
    BG_COLOR = "#1A1A1A"
    TEXT_COLOR = "#E0E0E0"
    ACCENT_COLOR = "#FF7B30"
    BUTTON_BG = "#2D2D2D"
    BUTTON_ACTIVE = "#8B0000"
    ENTRY_BG = "#2D2D2D"
    ENTRY_FG = "#FFFFFF"

    okno.configure(bg=BG_COLOR)
    
    if sys.platform.startswith('win'):
        if icon_ico and os.path.exists(icon_ico):
            okno.iconbitmap(icon_ico)
    else:
        if icon_png and os.path.exists(icon_png):
            try:
                img = tk.PhotoImage(file=icon_png)
                okno.iconphoto(True, img)
            except:
                pass


    # Стили
    TITLE_STYLE = {"font": ("Courier New", 28, "bold"), "bg": BG_COLOR, "fg": ACCENT_COLOR}
    LABEL_STYLE = {"font": ("Arial", 14, "bold"), "bg": BG_COLOR, "fg": TEXT_COLOR}
    ENTRY_STYLE = {"font": ("Courier New", 16, "bold"), "bg": ENTRY_BG, "fg": ENTRY_FG, "justify": "center", "bd": 2, "relief": "sunken"}
    BUTTON_STYLE = {
        "font": ("Arial", 16, "bold"),
        "width": 20,
        "height": 2,
        "bg": BUTTON_BG,
        "fg": ACCENT_COLOR,
        "activebackground": BUTTON_ACTIVE,
        "activeforeground": TEXT_COLOR,
        "relief": "raised",
        "bd": 3
    }
    BACK_BUTTON_STYLE = {
        "font": ("Arial", 14),
        "width": 3,
        "bg": BUTTON_BG,
        "fg": ACCENT_COLOR,
        "activebackground": BUTTON_ACTIVE,
        "activeforeground": TEXT_COLOR,
        "relief": "raised",
        "bd": 2
    }

    # Заголовок
    title_label = tk.Label(okno, text="🔌 ПОДКЛЮЧЕНИЕ К КОМНАТЕ 🔌", **TITLE_STYLE)
    title_label.pack(pady=(30, 20))

    # Кнопка назад
    back = tk.Button(okno, text="←", **BACK_BUTTON_STYLE, command=back_window)
    back.place(x=20, y=20)

    ip_label = tk.Label(okno, text="🌐 IP АДРЕС СЕРВЕРА (IP:PORT)", **LABEL_STYLE)
    ip_label.pack(pady=(10,5))

    ip_entry = tk.Entry(okno, **ENTRY_STYLE, width=25)
    ip_entry.pack(pady=5)

    # Ввод кода комнаты
    vvod = tk.Label(okno, text='🔑 ВВЕДИТЕ КОД КОМНАТЫ (CAPS)', **LABEL_STYLE)
    vvod.pack(pady=(40, 10))

    enter = tk.Entry(okno, **ENTRY_STYLE, width=20)
    enter.pack(pady=15)
    enter.focus()

    # Статус подключения
    status_label = tk.Label(okno, text="⏳ Ожидание кода...", **LABEL_STYLE)
    status_label.pack(pady=10)

    # Информация о бункере
    max_label = tk.Label(okno, text="⚡ Вместимость бункера: 0", **LABEL_STYLE)
    max_label.pack(pady=15)

    # Выбор номера игрока
    player_label = tk.Label(okno, text="🧍 ВЫБЕРИТЕ СВОЙ НОМЕР", **LABEL_STYLE)
    player_label.pack(pady=(30, 10))

    # Стилизация слайдера
    style = ttk.Style()
    style.configure("Horizontal.TScale", 
                   background=BG_COLOR,
                   troughcolor=BUTTON_BG,
                   bordercolor=ACCENT_COLOR,
                   darkcolor=ACCENT_COLOR,
                   lightcolor=ACCENT_COLOR)

    slider1 = ttk.Scale(okno, from_=1, to=maximum, orient="horizontal", length=400, style="Horizontal.TScale")
    slider1.set(1)
    slider1.pack(pady=20)

    label1 = tk.Label(okno, text="🧍 Ваш номер: 1", **LABEL_STYLE)
    label1.pack(pady=15)

    # Кнопка подключения
    connect_btn = tk.Button(okno, text="🚀 ПОДКЛЮЧИТЬСЯ", command=connection, **BUTTON_STYLE)
    connect_btn.pack(pady=40)

    # Поясняющий текст
    info_text = tk.Label(okno, 
                        text="⚠️ Введите код комнаты и выберите свой номер\n"
                             "Система автоматически проверит доступность",
                        font=("Arial", 12, "italic"),
                        bg=BG_COLOR,
                        fg="#A0A0A0",
                        justify="center")
    info_text.pack(pady=(30, 20))

    # Бинды
    slider1.bind("<Motion>", update_label1)
    slider1.bind("<ButtonRelease>", update_label1)
    enter.bind("<KeyRelease>", update_maximum_from_db)
    enter.bind("<<Paste>>", lambda e: okno.after(100, update_maximum_from_db))

    okno.mainloop()

if __name__ == '__main__':
    connect()
