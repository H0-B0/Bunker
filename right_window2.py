import sqlite3 as sq
import tkinter as tk
import os
import sys

# Основная функция
def right1(code, icon_png, icon_ico, db_path):
    
    # Получение кода комнаты из переданной БД
    with sq.connect(db_path) as dannie:  # ← ВАЖНО: используй db_path
        cur = dannie.cursor()
        cur.execute("SELECT max_players,years,mesto,ploshad FROM rooms WHERE code = ?",(code,))
        data = cur.fetchall()
        
        # Получение максимального количества игроков для данной комнаты
        players = data[0][0]

    # Стиль апокалипсиса
    BG_COLOR = "#1A1A1A"  # Тёмно-серый, почти чёрный
    TEXT_COLOR = "#E0E0E0"  # Светло-серый
    ACCENT_COLOR = "#FF7B30"  # Ржавый оранжевый
    BUTTON_BG = "#2D2D2D"  # Тёмно-серый для кнопок
    BUTTON_ACTIVE = "#CC5500"  # Тёмно-оранжевый при нажатии
    
    ZAGOLOVOK_STYLE = {"font": ("Arial", 12, "bold"), "bg": BG_COLOR, 'fg':ACCENT_COLOR}
    BUTTON_STYLE = {"font": ("Arial", 12), "bg": BG_COLOR, 'fg' : TEXT_COLOR}
    STYLE = {"font": ("Arial", 12), "bg": BG_COLOR, 'fg' : 'darkorange'}

    # Создание дочернего окна поверх других
    okno = tk.Toplevel()
    okno.configure(background=BG_COLOR)
    okno.geometry('450x700')

    # Взависимости от системы ставится иконка
    if sys.platform.startswith('win'):
        if icon_ico and os.path.exists(icon_ico):
            okno.iconbitmap(icon_ico)
    else:
        if icon_png and os.path.exists(icon_png):
            try:
                img = tk.PhotoImage(file=icon_png)
                okno.iconphoto(True, img)
            except: pass

    # Контент
    rounds = tk.Label(okno, text='Раунды',**ZAGOLOVOK_STYLE)
    rounds.grid(column=1, row=0)

    # Взависимости от того, сколько игроков ставится количество раундов с изгнанием игроков. Раскрытие карт не меняется
    if players == 4:
        for4_players = tk.Label(okno,text="""Изгнать игроков:
                                
Открыть карт:""",**ZAGOLOVOK_STYLE)
        for4_players.grid(column=0,row=1, pady=(10,0),padx=(27,0))

        izgnanie = tk.Label(okno, text='''0   0   1   1
----------------
1   1   2   2''',**BUTTON_STYLE)
        izgnanie.grid(column=1,row=1,pady=(10,0))

    elif players == 6 or players == 5:
        for4_players = tk.Label(okno,text="""Изгнать игроков:
                                
Открыть карт:""",**ZAGOLOVOK_STYLE)
        for4_players.grid(column=0,row=1, pady=(10,0),padx=(27,0))

        izgnanie = tk.Label(okno, text='''0   1   1   1
----------------
1   1   2   2''',**BUTTON_STYLE)
        izgnanie.grid(column=1,row=1,pady=(10,0))


    elif players == 7 or players == 8:
        for4_players = tk.Label(okno,text="""Изгнать игроков:
                                
Открыть карт:""",**ZAGOLOVOK_STYLE)
        for4_players.grid(column=0,row=1, pady=(10,0),padx=(27,0))

        izgnanie = tk.Label(okno, text='''1   1   1   1
---------------
1   1   2   2''',**BUTTON_STYLE) 
        izgnanie.grid(column=1,row=1,pady=(10,0))


    elif players == 9 or players == 10:


        for4_players = tk.Label(okno,text="""Изгнать игроков:
                                
Открыть карт:""",**ZAGOLOVOK_STYLE)
        for4_players.grid(column=0,row=1, pady=(10,0),padx=(27,0))

        izgnanie = tk.Label(okno, text='''1   1   1   2
----------------
1   1   2   2''',**BUTTON_STYLE)
        izgnanie.grid(column=1,row=1,pady=(10,0))

    separator1 = tk.Frame(okno, height=2, width=200, bg=ACCENT_COLOR)
    separator1.grid(column=0, columnspan=3, row=2, sticky='we', padx=30, pady=10)

    if players <= 7:
        mission = tk.Label(okno,text="Цели:",**ZAGOLOVOK_STYLE)
        mission.grid(column=0, row=4, pady=(10,0),padx=(27,0))

        missions = tk.Label(okno,text="Попасть в бункер",**BUTTON_STYLE)
        missions.grid(column=1, row=4, pady=(10,0))

    elif players >= 8:
        mission = tk.Label(okno,text="Цели:",**ZAGOLOVOK_STYLE)
        mission.grid(column=0, row=4, pady=(10,0),padx=(27,0),sticky='n')

        missions = tk.Label(okno,text="Попасть в бункер\n\nПродолжить род",**BUTTON_STYLE)
        missions.grid(column=1, row=4, pady=(10,0))

if __name__ == "__main__":
    right1("DMA")
