import tkinter as tk
from tkinter import ttk
import os
import sys
import socket
import requests
import threading
import time
import traceback
from universal_okno import game_okno


# Получение БД и картинок
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Основная функция
def sozdat(icon_png, icon_ico, db_path=None):
    # Создание окна
    okno = tk.Tk()
    okno.geometry('1200x1000')
    okno.title('Бункер')

    # Взависимости от системы ставится полноэкранный режим
    if sys.platform.startswith('win'):
        okno.state('zoomed')
    else:
        try:
            okno.attributes('-zoomed', True)
        except:
            okno.state('normal')

    # Цвета
    BG_COLOR = "#1A1A1A"
    TEXT_COLOR = "#E0E0E0"
    ACCENT_COLOR = "#FF7B30"
    BUTTON_BG = "#2D2D2D"
    BUTTON_ACTIVE = "#8B0000"

    okno.configure(bg=BG_COLOR)

    # Взависимости от системы ставится иконка
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

    # Начальные данные
    value1 = 4
    value2 = 1
    server_ip = '127.0.0.1:8000'

    # Главная функция
    def made():
        nonlocal value1, value2, server_ip
        # Получение IP
        server_ip = ip_entry.get().strip()
        if not server_ip:
            server_ip = '127.0.0.1:8000'

        if ':' in server_ip:
            host, port = server_ip.split(':')
        else:
            host = server_ip
            port = '8000'

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, int(port)))
        sock.close()

        # АВТОМАТИЧЕСКИЙ ЗАПУСК СЕРВЕРА
        if result != 0:
            try:
                import uvicorn
                from server import app

                def run_server():
                    uvicorn.run(app, host=host, port=int(port), log_level="critical", access_log=False, log_config=None)

                thread = threading.Thread(target=run_server, daemon=True)
                thread.start()
                time.sleep(1)
            except Exception as e:
                with open("server_start_crash.log", "w") as f:
                    traceback.print_exc(file=f)
                raise

        okno.destroy()

        game_okno(value2, icon_png, icon_ico, db_path, value1, '', server_ip)

    def update_label1(event=None):
        # Обновление ролла с количеством игроков
        nonlocal value1, value2
        value = slider1.get()
        value1 = int(value)
        label1.config(text=f"⚡ Количество игроков: {value1}")
        slider2.config(to=value1)
        if value2 > value1:
            value2 = value1
            slider2.set(value1)
            label2.config(text=f"🧍 Ваш номер в бункере: {value2}")

    def update_label2(event=None):
        # Обновление ролла с номером игрока
        nonlocal value2
        value = slider2.get()
        value2 = int(value)
        label2.config(text=f"🧍 Ваш номер в бункере: {value2}")

    # Кнопка выхода в подделку main
    def back_window():
        okno.destroy()
        import podmain
        podmain.podmaini(icon_png, icon_ico, db_path)

    # Стили
    TITLE_STYLE = {"font": ("Courier New", 28, "bold"), "bg": BG_COLOR, "fg": ACCENT_COLOR}
    LABEL_STYLE = {"font": ("Arial", 16, "bold"), "bg": BG_COLOR, "fg": TEXT_COLOR}
    ENTRY_STYLE = {"font": ("Courier New", 14, "bold"), "bg": BUTTON_BG, "fg": TEXT_COLOR,
                   "justify": "center", "bd": 2, "relief": "sunken"}
    BUTTON_STYLE = {
        "font": ("Arial", 16, "bold"),
        "width": 25,
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

    # Контент
    title_label = tk.Label(okno, text="🚧 СОЗДАНИЕ БУНКЕРА 🚧", **TITLE_STYLE)
    title_label.pack(pady=(30, 20))
    back = tk.Button(okno, text="←", **BACK_BUTTON_STYLE, command=back_window)
    back.place(x=20, y=20)
    ip_label = tk.Label(okno, text="🌐 IP АДРЕС СЕРВЕРА (IP:PORT)", **LABEL_STYLE)
    ip_label.pack(pady=(10,5))
    ip_entry = tk.Entry(okno, **ENTRY_STYLE, width=25)
    ip_entry.pack(pady=5)

    style = ttk.Style()
    style.configure("Horizontal.TScale",
                    background=BG_COLOR,
                    troughcolor=BUTTON_BG,
                    bordercolor=ACCENT_COLOR,
                    darkcolor=ACCENT_COLOR,
                    lightcolor=ACCENT_COLOR)

    slider1 = ttk.Scale(okno, from_=4, to=10, orient="horizontal", length=500, style="Horizontal.TScale")
    slider1.set(4)
    slider1.pack(pady=(50, 10))
    label1 = tk.Label(okno, text="⚡ Количество игроков: 4", **LABEL_STYLE)
    label1.pack(pady=(0, 40))

    slider2 = ttk.Scale(okno, from_=1, to=value1, orient="horizontal", length=500, style="Horizontal.TScale")
    slider2.set(1)
    slider2.pack(pady=(30, 10))
    label2 = tk.Label(okno, text="🧍 Ваш номер в бункере: 1", **LABEL_STYLE)
    label2.pack(pady=(0, 50))

    create = tk.Button(okno, text='🚀 СОЗДАТЬ БУНКЕР', command=made, **BUTTON_STYLE)
    create.pack(pady=30)

    info_text = tk.Label(okno,
                         text="⚠️ Выберите количество игроков и ваш номер в бункере\n"
                              "⚠️ Введите IP адрес сервера (Например 1.1.1.1:0000)\n"
                              "Система автоматически распределит характеристики",
                         font=("Arial", 12, "italic"), bg=BG_COLOR, fg="#A0A0A0", justify="center")
    info_text.pack(pady=(40, 20))

    slider1.bind("<Motion>", update_label1)
    slider1.bind("<ButtonRelease>", update_label1)
    slider2.bind("<Motion>", update_label2)
    slider2.bind("<ButtonRelease>", update_label2)

    okno.mainloop()

if __name__ == '__main__':
    sozdat(None, None, None)