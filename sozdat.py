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
import subprocess
import socket
import time
import atexit

server_process = None

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def stop_server():
    global server_process
    if server_process:
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()
        except Exception as e:
            print(f'Ошибка при остановке сервера - {e}')
        finally:
            server_process = None

def sozdat(icon_png, icon_ico, db_path=None):
    global server_process
    
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

    def on_closing():
        stop_server()
        okno.destroy()

    okno.protocol("WM_DELETE_WINDOW", on_closing)

    atexit.register(stop_server)

    # Стиль апокалипсиса
    BG_COLOR = "#1A1A1A"  # Тёмно-серый, почти чёрный
    TEXT_COLOR = "#E0E0E0"  # Светло-серый
    ACCENT_COLOR = "#FF7B30"  # Ржавый оранжевый
    SLIDER_COLOR = "#CC5500"  # Тёмно-оранжевый
    BUTTON_BG = "#2D2D2D"  # Тёмно-серый для кнопок
    BUTTON_ACTIVE = "#8B0000"  # Тёмно-красный при нажатии

    okno.configure(bg=BG_COLOR)
    
    if sys.platform.startswith('win'):
        if icon_ico and os.path.exists(icon_ico):
            okno.iconbitmap(icon_ico)
    else:
        if icon_png and os.path.exists(icon_png):
            try:
                img = tk.PhotoImage(file=icon_png)
                okno.iconphoto(True, img)
            except: pass

    value1 = 4
    value2 = 1
    server_ip = '127.0.0.1:8000'

    def made():
        nonlocal value1, value2, server_ip
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

        if result != 0:
            global server_process
            server_process = subprocess.Popen([sys.executable, '-m', 'uvicorn','server:app', '--host', host, '--port', port], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
        else: print('Сервер уже запущен')
        okno.destroy()
        print(f"Создаем комнату: {value1} игроков, я игрок №{value2}, сервер: {server_ip}")
        if value1 == 4:
            okno4(value2, icon_png, icon_ico, db_path, '', server_ip)
        elif value1 == 5:
            okno5(value2, icon_png, icon_ico, db_path, '', server_ip)
        elif value1 == 6:
            okno6(value2, icon_png, icon_ico, db_path, '', server_ip)
        elif value1 == 7:
            okno7(value2, icon_png, icon_ico, db_path, '', server_ip)
        elif value1 == 8:
            okno8(value2, icon_png, icon_ico, db_path, '', server_ip)
        elif value1 == 9:
            okno9(value2, icon_png, icon_ico, db_path, '', server_ip)
        elif value1 == 10:
            okno10(value2, icon_png, icon_ico, db_path, '', server_ip)

    def update_label1(event=None):
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
        nonlocal value2
        value = slider2.get()
        value2 = int(value)
        label2.config(text=f"🧍 Ваш номер в бункере: {value2}")

    def back_window():
        stop_server()
        okno.destroy()
        import podmain
        podmain.podmaini(icon_png, icon_ico, db_path)

    # Стили
    TITLE_STYLE = {"font": ("Courier New", 28, "bold"), "bg": BG_COLOR, "fg": ACCENT_COLOR}
    LABEL_STYLE = {"font": ("Arial", 16, "bold"), "bg": BG_COLOR, "fg": TEXT_COLOR}
    ENTRY_STYLE = {"font": ("Courier New", 14, "bold"), "bg": BUTTON_BG, "fg": TEXT_COLOR, "justify": "center", "bd": 2, "relief": "sunken"}
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

    # Заголовок
    title_label = tk.Label(okno, text="🚧 СОЗДАНИЕ БУНКЕРА 🚧", **TITLE_STYLE)
    title_label.pack(pady=(30, 20))

    # Кнопка назад
    back = tk.Button(okno, text="←", **BACK_BUTTON_STYLE, command=back_window)
    back.place(x=20, y=20)

    ip_label = tk.Label(okno, text="🌐 IP АДРЕС СЕРВЕРА (IP:PORT)", **LABEL_STYLE)
    ip_label.pack(pady=(10,5))

    ip_entry = tk.Entry(okno, **ENTRY_STYLE, width=25)
    ip_entry.pack(pady=5)

    # Настройка стиля слайдеров
    style = ttk.Style()
    style.configure("Horizontal.TScale", 
                   background=BG_COLOR,
                   troughcolor=BUTTON_BG,
                   bordercolor=ACCENT_COLOR,
                   darkcolor=ACCENT_COLOR,
                   lightcolor=ACCENT_COLOR)

    # Первый слайдер - количество игроков
    slider1 = ttk.Scale(okno, from_=4, to=10, orient="horizontal", length=500, style="Horizontal.TScale")
    slider1.set(4)
    slider1.pack(pady=(50, 10))

    label1 = tk.Label(okno, text="⚡ Количество игроков: 4", **LABEL_STYLE)
    label1.pack(pady=(0, 40))

    # Второй слайдер - номер игрока
    slider2 = ttk.Scale(okno, from_=1, to=value1, orient="horizontal", length=500, style="Horizontal.TScale")
    slider2.set(1)
    slider2.pack(pady=(30, 10))

    label2 = tk.Label(okno, text="🧍 Ваш номер в бункере: 1", **LABEL_STYLE)
    label2.pack(pady=(0, 50))

    # Кнопка создания комнаты
    create = tk.Button(okno, text='🚀 СОЗДАТЬ БУНКЕР', command=made, **BUTTON_STYLE)
    create.pack(pady=30)

    # Поясняющий текст
    info_text = tk.Label(okno, 
                        text="⚠️ Выберите количество игроков и ваш номер в бункере\n"
                             "⚠️ Введите IP адрес сервера (Например 1.1.1.1:0000)\n"
                             "Система автоматически распределит характеристики",
                        font=("Arial", 12, "italic"),
                        bg=BG_COLOR,
                        fg="#A0A0A0",
                        justify="center")
    info_text.pack(pady=(40, 20))

    # Бинды для слайдеров
    slider1.bind("<Motion>", update_label1)
    slider1.bind("<ButtonRelease>", update_label1)
    slider2.bind("<Motion>", update_label2)
    slider2.bind("<ButtonRelease>", update_label2)

    okno.mainloop()

if __name__ == '__main__':
    sozdat()