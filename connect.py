import sqlite3 as sq
import tkinter as tk
from tkinter import ttk
from universal_okno import game_okno
import os
import sys
import requests

# Нахождение БД и иконок
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Основная функция
def connect(icon_png, icon_ico, db_path):
    
    print(f"connect: db_path = {db_path}")
    print(f"connect: db exists = {os.path.exists(db_path) if db_path else False}")
    
    #Начальные данные, до заполнения
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
        check_occupied_numbers()  # Проверяем при изменении номера

    #Изменения максимального числа игроков мониторя БД
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
                                slider1.set(1)
                                update_label1()
                            max_label.config(text=f"⚡ Вместимость бункера: {maximum}", fg="#00FF00")
                            status_label.config(text="✅ Бункер обнаружен", fg="#00FF00")
                            check_occupied_numbers()
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
            connect_btn.config(state="normal", text="🚀 ПОДКЛЮЧИТЬСЯ", bg=BUTTON_BG)
            error_label.config(text="")
        game_code = enter.get()

    #Проверяет занятые номера и обновляет состояние кнопки
    def check_occupied_numbers():
        code = enter.get().strip().upper()
        ip = ip_entry.get().strip()
        
        # Если нет IP или кода — не проверяем
        if not ip or not code or len(code) < 2 or maximum == 0:
            connect_btn.config(state="normal", text="🚀 ПОДКЛЮЧИТЬСЯ", bg=BUTTON_BG)
            error_label.config(text="")
            status_label.config(text="⏳ Ожидание данных...", fg="#A0A0A0")
            return
        
        try:
            response = requests.get(f"http://{ip}/rooms/{code}/players", timeout=2)
            if response.status_code == 200:
                occupied = response.json()
                current_number = int(slider1.get())
                
                if current_number in occupied:
                    connect_btn.config(state="disabled", text="❌ Номер занят", bg="#444444")
                    error_label.config(text="⚠️ Номер занят другим игроком!", fg="#FF0000")
                    status_label.config(text="⚠️ Выберите другой номер", fg="#FF7B30")
                else:
                    connect_btn.config(state="normal", text="🚀 ПОДКЛЮЧИТЬСЯ", bg=BUTTON_BG)
                    error_label.config(text="✅ Номер свободен", fg="#00FF00")
                    status_label.config(text="✅ Можно подключаться", fg="#00FF00")
            else:
                connect_btn.config(state="normal", text="🚀 ПОДКЛЮЧИТЬСЯ", bg=BUTTON_BG)
                error_label.config(text="⚠️ Комната не найдена", fg="#FF7B30")
                status_label.config(text="⚠️ Проверьте код", fg="#FF7B30")
        except requests.exceptions.ConnectionError:
            connect_btn.config(state="normal", text="🚀 ПОДКЛЮЧИТЬСЯ", bg=BUTTON_BG)
            error_label.config(text="⚠️ Сервер не отвечает", fg="#FF7B30")
            status_label.config(text="⚠️ Проверьте IP и сервер", fg="#FF7B30")
        except Exception as e:
            print(f"Ошибка проверки занятых номеров: {e}")
            connect_btn.config(state="normal", text="🚀 ПОДКЛЮЧИТЬСЯ", bg=BUTTON_BG)
            error_label.config(text="⚠️ Ошибка соединения", fg="#FF7B30")
            status_label.config(text="⚠️ Проверьте IP", fg="#FF7B30")

    #Вызывается, если IP изменяется
    def on_ip_change(event=None):
        check_occupied_numbers()

    # Главная функция
    def connection():
        nonlocal maximum, game_code, player, server_ip
        server_ip = ip_entry.get().strip()
        if not server_ip:
            server_ip = '127.0.0.1:8000'
        
        # Проверяем, занят ли номер перед подключением
        code = enter.get().strip().upper()
        if code and len(code) >= 2:
            try:
                response = requests.get(f"http://{server_ip}/rooms/{code}/players", timeout=2)
                if response.status_code == 200:
                    occupied = response.json()
                    if player in occupied:
                        error_label.config(text="❌ Этот номер уже занят!", fg="#FF0000")
                        return
            except:
                pass
        
        okno.destroy()

        game_okno(player, icon_png, icon_ico, db_path, maximum, game_code, server_ip)
        
    # Функция для возвращения в подобие main
    def back_window():
        okno.destroy()
        import podmain
        podmain.podmaini(icon_png, icon_ico, db_path)

    # Создание окна
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
    
    # Выбор иконки взависимости от системы
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

    # ========== ПРОКРУТКА (исправленная) ==========
    main_frame = tk.Frame(okno, bg=BG_COLOR)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.configure(bg=BG_COLOR, troughcolor=BG_COLOR, activebackground=BG_COLOR, width=0)

    content_frame = tk.Frame(canvas, bg=BG_COLOR)
    canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def configure_scrollregion(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.update_idletasks()
        if content_frame.winfo_reqwidth() < canvas.winfo_width():
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        # Показываем скроллбар, если высота окна меньше 1000
        if okno.winfo_height() < 1000:
            if not scrollbar.winfo_ismapped():
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        else:
            if scrollbar.winfo_ismapped():
                scrollbar.pack_forget()
                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                canvas.yview_moveto(0.0)

    def on_mousewheel(event):
        if not scrollbar.winfo_ismapped():
            return
        if sys.platform.startswith('win'):
            delta = -1 * (event.delta // 120)
        else:
            if event.num == 4:
                delta = -1
            elif event.num == 5:
                delta = 1
            else:
                delta = 0
        if delta != 0:
            canvas.yview_scroll(delta, "units")
        return "break"

    # Глобальная привязка ко всем окнам
    if sys.platform.startswith('win'):
        okno.bind_all("<MouseWheel>", on_mousewheel)
    else:
        okno.bind_all("<Button-4>", on_mousewheel)
        okno.bind_all("<Button-5>", on_mousewheel)

    content_frame.bind("<Configure>", configure_scrollregion)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=canvas.winfo_width()))

    # Упаковываем canvas
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Привязываем изменение размера окна
    okno.bind("<Configure>", lambda e: configure_scrollregion())
    # ========== КОНЕЦ ПРОКРУТКИ ==========

    # Разметка
    title_label = tk.Label(content_frame, text="🔌 ПОДКЛЮЧЕНИЕ К КОМНАТЕ 🔌", **TITLE_STYLE)
    title_label.pack(pady=(30, 20))

    back = tk.Button(okno, text="←", **BACK_BUTTON_STYLE, command=back_window)
    back.place(x=20, y=20)

    ip_label = tk.Label(content_frame, text="🌐 IP АДРЕС СЕРВЕРА (IP:PORT)", **LABEL_STYLE)
    ip_label.pack(pady=(10,5))
    ip_entry = tk.Entry(content_frame, **ENTRY_STYLE, width=25)
    ip_entry.pack(pady=5)
    ip_entry.bind("<KeyRelease>", on_ip_change)
    ip_entry.bind("<<Paste>>", lambda e: okno.after(100, on_ip_change))

    vvod = tk.Label(content_frame, text='🔑 ВВЕДИТЕ КОД КОМНАТЫ (CAPS)', **LABEL_STYLE)
    vvod.pack(pady=(40, 10))
    enter = tk.Entry(content_frame, **ENTRY_STYLE, width=20)
    enter.pack(pady=15)
    enter.focus()

    status_label = tk.Label(content_frame, text="⏳ Ожидание кода...", **LABEL_STYLE)
    status_label.pack(pady=10)

    max_label = tk.Label(content_frame, text="⚡ Вместимость бункера: 0", **LABEL_STYLE)
    max_label.pack(pady=15)

    player_label = tk.Label(content_frame, text="🧍 ВЫБЕРИТЕ СВОЙ НОМЕР", **LABEL_STYLE)
    player_label.pack(pady=(30, 10))

    style = ttk.Style()
    style.configure("Horizontal.TScale", 
                   background=BG_COLOR,
                   troughcolor=BUTTON_BG,
                   bordercolor=ACCENT_COLOR,
                   darkcolor=ACCENT_COLOR,
                   lightcolor=ACCENT_COLOR)

    slider1 = ttk.Scale(content_frame, from_=1, to=maximum, orient="horizontal", length=400, style="Horizontal.TScale")
    slider1.set(1)
    slider1.pack(pady=20)

    label1 = tk.Label(content_frame, text="🧍 Ваш номер: 1", **LABEL_STYLE)
    label1.pack(pady=15)

    # --- БЛОК ПРОВЕРКИ ЗАНЯТЫХ НОМЕРОВ ---
    error_label = tk.Label(content_frame, text="", **LABEL_STYLE)
    error_label.pack(pady=5)

    connect_btn = tk.Button(content_frame, text="🚀 ПОДКЛЮЧИТЬСЯ", command=connection, **BUTTON_STYLE)
    connect_btn.pack(pady=40)

    # Привязка событий
    slider1.bind("<ButtonRelease>", update_label1)
    slider1.bind("<Motion>", update_label1)
    enter.bind("<KeyRelease>", update_maximum_from_db)
    enter.bind("<<Paste>>", lambda e: content_frame.after(100, update_maximum_from_db))

    info_text = tk.Label(content_frame, 
                        text="⚠️ Введите код комнаты и выберите свой номер\n"
                             "Система автоматически проверит доступность",
                        font=("Arial", 12, "italic"),
                        bg=BG_COLOR,
                        fg="#A0A0A0",
                        justify="center")
    info_text.pack(pady=(30, 20))

    # Принудительное обновление прокрутки
    okno.update_idletasks()
    configure_scrollregion()
    okno.mainloop()

if __name__ == '__main__':
    connect()