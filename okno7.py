import tkinter as tk
import random as r
import sqlite3 as sq
from left_window import left
from right_window1 import right2
from right_window2 import right1
import os
import sys
from tkinter.messagebox import showerror
import requests
import threading
import time

# Список игроков и начальных данных
play = {
"igrok1":{
"Профессия":"hidden",
"Биология":"hidden",
"Здоровье":"hidden",
"Хобби":"hidden",
"Фобия":"hidden",
"Характер":"hidden",
"Факты":"hidden",
"Багаж":"hidden",
"Условие":"hidden"},
"igrok2":{
"Профессия":"hidden",
"Биология":"hidden",
"Здоровье":"hidden",
"Хобби":"hidden",
"Фобия":"hidden",
"Характер":"hidden",
"Факты":"hidden",
"Багаж":"hidden",
"Условие":"hidden"},
"igrok3":{
"Профессия":"hidden",
"Биология":"hidden",
"Здоровье":"hidden",
"Хобби":"hidden",
"Фобия":"hidden",
"Характер":"hidden",
"Факты":"hidden",
"Багаж":"hidden",
"Условие":"hidden"},
"igrok4":{
"Профессия":"hidden",
"Биология":"hidden",
"Здоровье":"hidden",
"Хобби":"hidden",
"Фобия":"hidden",
"Характер":"hidden",
"Факты":"hidden",
"Багаж":"hidden",
"Условие":"hidden"},
"igrok5":{
"Профессия":"hidden",
"Биология":"hidden",
"Здоровье":"hidden",
"Хобби":"hidden",
"Фобия":"hidden",
"Характер":"hidden",
"Факты":"hidden",
"Багаж":"hidden",
"Условие":"hidden"},
"igrok6":{
"Профессия":"hidden",
"Биология":"hidden",
"Здоровье":"hidden",
"Хобби":"hidden",
"Фобия":"hidden",
"Характер":"hidden",
"Факты":"hidden",
"Багаж":"hidden",
"Условие":"hidden"},
"igrok7":{
"Профессия":"hidden",
"Биология":"hidden",
"Здоровье":"hidden",
"Хобби":"hidden",
"Фобия":"hidden",
"Характер":"hidden",
"Факты":"hidden",
"Багаж":"hidden",
"Условие":"hidden"}
}

# Нааходим БД и картинки
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#Основная функция
def okno7(player, icon_png, icon_ico, db_path, code='', server_ip='127.0.0.1:8000'):
    
    print(f"okno7: db_path = {db_path}")
    print(f"okno7: db exists = {os.path.exists(db_path) if db_path else False}")
    print(f"okno7: server_ip = {server_ip}")

    #Если код комнаты пустой(То есть она создается), то берем рандомную по количеству игроков и извлекаем из нее данные
    try:
        with sq.connect(db_path) as dannie:
            cur = dannie.cursor()
            if code == '':
                cur.execute('''
                    SELECT room_id FROM (
                        SELECT room_id, COUNT(player_id) as player_count
                        FROM svazka
                        GROUP BY room_id
                        HAVING COUNT(player_id) = 7
                    )
                    ORDER BY RANDOM()
                    LIMIT 1
                ''')

                id_room = cur.fetchall()
                # Нужно для того, чтобы выделить случайную комнату в которой есть 7 игроков

                # Получайем id комнаты
                cur.execute("SELECT * FROM rooms WHERE id = ?",(id_room[0]))
            else:
                cur.execute("SELECT * FROM rooms WHERE code = ?",(code,))

            room_info = cur.fetchall()

            print(room_info)

            id_room = room_info[0]

            code = room_info[0][1]
            # Получайем id комнаты

            # Получаем id игроков в этой комнате по средством связи
            cur.execute("SELECT player_id FROM svazka WHERE room_id = ?",(id_room[0],))

            players_id = cur.fetchall()
            # Получаем id игроков в этой комнате по средством связи

            # Через id игроков получаем всю инфу о них, и записываем в список
            players = []

            for i in players_id:
                for j in i:
                    cur.execute("SELECT profession,biology,health,hobby,fobya,character,fact,bagaje,uslovie FROM players WHERE id = ?",(j,))
                    players.append(list(*cur.fetchall()))
                    break

        player1 = players[0]
        player2 = players[1]
        player3 = players[2]
        player4 = players[3]
        player5 = players[4]
        player6 = players[5]
        player7 = players[6]

        #Закидываем на сервер информацию о игроках
        requests.post(f'http://{server_ip}/rooms/{code}', json={'play':play})

        # СТИЛЬ АПОКАЛИПСИСА
        BG_COLOR = "#1A1A1A"  # Тёмный фон
        TEXT_COLOR = "#E0E0E0"  # Светлый текст
        ACCENT_COLOR = "#FF7B30"  # Оранжевые акценты
        BUTTON_BG = "#2D2D2D"  # Фон кнопок
        BUTTON_ACTIVE = "#CC5500"  # Активные кнопки
        RED_ACCENT = "#8B0000"  # Красный для кнопок изгнания
        GREEN_ACCENT = "#00AA00"  # Зелёный для чекбоксов

        # Стили
        HEADING_STYLE = {"font": ("Courier New", 14, "bold"), "bg": BG_COLOR, "fg": ACCENT_COLOR}
        ZAGOLOVOK_STYLE = {"font": ("Arial", 12, "bold"), "bg": BG_COLOR}
        BUTTON_STYLE = {
            "font": ("Arial", 12), 
            "width": 44,
            "bg": BG_COLOR,
            "fg": ACCENT_COLOR,
            "activebackground": BUTTON_ACTIVE,
            "activeforeground": TEXT_COLOR,
            "relief": "raised",
            "bd": 2,
            "wraplength":400,
            "justify":"left"
        }
        PADDING = {"pady": 5}
        IZGON_STYLE = {"font": ("Arial", 12, "bold"), "bg": BG_COLOR, "fg": RED_ACCENT}
        SPECIAL_BUTTON_STYLE = {"font": ("Arial", 16), "bg": "#4A4A2A", "fg": "yellow", "width": 3, "height": 1}

        # Создаем главное окно
        window = tk.Tk()
        window.title("Бункер")
        window.geometry("1200x1000")
        window.configure(bg=BG_COLOR)

        window.withdraw()
        window.update_idletasks()

        # Взависимости от системы берем иконку
        if sys.platform.startswith('win'):
            if icon_ico and os.path.exists(icon_ico):
                window.iconbitmap(icon_ico)
        else:
            if icon_png and os.path.exists(icon_png):
                try:
                    img = tk.PhotoImage(file=icon_png)
                    window.iconphoto(True, img)
                except: pass

        #Кидаем на сервер список, где все игроки еще в бункере
        array = [1,2,3,4,5,6,7]
        requests.post(f'http://{server_ip}/rooms/{code}/spisok', json={'data':array})

        # ПРОСТАЯ РАБОЧАЯ СИСТЕМА ПРОКРУТКИ
        # Создаем основной контейнер
        main_frame = tk.Frame(window, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем Canvas и Scrollbar
        canvas = tk.Canvas(main_frame, bg=BG_COLOR, highlightthickness=0)
        # Создаем НЕВИДИМЫЙ Scrollbar
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.configure(
            bg=BG_COLOR,  # тот же цвет что и у фона
            troughcolor=BG_COLOR,
            activebackground=BG_COLOR,
            width=0  # делаем совсем тонким
        )

        # Создаем фрейм для контента
        content_frame = tk.Frame(canvas, bg=BG_COLOR)

        # Привязываем фрейм к canvas
        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Переменная для отслеживания состояния прокрутки
        scroll_enabled = False

        def configure_scrollregion(event=None):
            # Обновляем область прокрутки
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            # Центрируем контент по горизонтали
            canvas.update_idletasks()
            if content_frame.winfo_reqwidth() < canvas.winfo_width():
                canvas.itemconfig(canvas_window, width=canvas.winfo_width())
            
            # Проверяем высоту окна для включения/выключения прокрутки
            window_height = window.winfo_height()
            nonlocal scroll_enabled
            
            if window_height <= 855:  # Включаем прокрутку
                if not scroll_enabled:
                    scroll_enabled = True
                    # НЕ показываем скроллбар визуально, но оставляем функциональным
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            else:  # Выключаем прокрутку
                if scroll_enabled:
                    scroll_enabled = False
                    scrollbar.pack_forget()
                    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    canvas.yview_moveto(0.0)

        # Функция для прокрутки колесом мыши
        def on_mousewheel(event):
            if scroll_enabled:
                if sys.platform.startswith('win'):
                    delta = int(-1* (event.delta / 120))
                else:
                    if event.num == 4:
                        delta = -1
                    elif event.num == 5:
                        delta = 1
                    else:
                        delta = 0
                canvas.yview_scroll(delta, "units")

        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw", tags="content_frame")
        
        # Привязываем события
        content_frame.bind("<Configure>", configure_scrollregion)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=canvas.winfo_width()))
        canvas.bind("<MouseWheel>", on_mousewheel)

        # Упаковываем canvas (scrollbar будет добавляться/убираться динамически)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Также отслеживаем изменение размера окна
        def on_window_resize(event):
            if event.widget == window:  # Только если изменилось главное окно
                configure_scrollregion()

        window.bind("<Configure>", on_window_resize)

        # Функция меняющая количество игроков
        def zamena():
            user1.count.config(text=f'{len(array)}/3 людей')
            user2.count.config(text=f'{len(array)}/3 людей') 
            user3.count.config(text=f'{len(array)}/3 людей')
            user4.count.config(text=f'{len(array)}/3 людей')
            user5.count.config(text=f'{len(array)}/3 людей')
            user6.count.config(text=f'{len(array)}/3 людей')
            user7.count.config(text=f'{len(array)}/3 людей')

        # Функция убирающая игрока, если окно закрывается
        def on_closing():
            # try для того, чтобы если сервер выключен, можно было закрыть окно
            try:
                requests.post(f'http://{server_ip}/rooms/{code}/players/del', json={'player':player})
            except Exception:
                pass
            window.destroy()

        # Класс игрока
        class Player:
            # Бинд главных переменых
            def __init__(self,massiv,number):
                # Внутренняя инфа
                self.massiv = massiv
                self.number = number
                self.db_path = db_path
                self.code = code

                # Профессии
                self.profession = None
                self.biology = None
                self.health = None
                self.hobby = None
                self.fobya = None
                self.chara = None
                self.fact = None
                self.bagaje = None
                self.uslovie = None

                # Чекбоксы
                self.prof = tk.IntVar()
                self.bio = tk.IntVar()
                self.heal = tk.IntVar()
                self.hoby = tk.IntVar()
                self.fobia = tk.IntVar()
                self.char = tk.IntVar()
                self.fiact = tk.IntVar()
                self.bag = tk.IntVar()
                self.usl = tk.IntVar()

            # ФУНКЦИИ КНОПОК
            def right_window(self):
                if len(array) != 3:
                    showerror(title='Ошибка',message='Чтобы открыть угрозу в комнате должно остаться 2 игрока')
                else:
                    right2(room_info[0][1], icon_png, icon_ico, db_path)

            def not_goden(self):
                hz = self.yes_or_not.cget('text')
                if hz == '':
                    self.yes_or_not.config(text='НЕ ГОДЕН', fg=RED_ACCENT)
                    self.izgnanie.config(text='ВЕРНУТЬ',fg="#00E400")
                    array.remove(self.number)
                    requests.post(f'http://{server_ip}/rooms/{code}/spisok', json={'data':array})
                elif hz == 'НЕ ГОДЕН':
                    self.yes_or_not.config(text='', fg=RED_ACCENT)
                    self.izgnanie.config(text='ИЗГНАТЬ',fg=RED_ACCENT)
                    array.append(self.number)
                    requests.post(f'http://{server_ip}/rooms/{code}/spisok', json={'data':array})
                zamena()

            def _vikid(self):
                self.yes_or_not.config(text='НЕ ГОДЕН', fg=RED_ACCENT)
                self.izgnanie.config(text='ВЕРНУТЬ',fg="#00E400")

            def prof_button(self):
                if self.prof.get() == 0:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Профессия', 'value':'hidden'})
                else:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Профессия', 'value':self.massiv[0]})

            def bio_button(self):
                if self.bio.get() == 0:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Биология', 'value':'hidden'})
                else:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Биология', 'value':self.massiv[1]})

            def heal_button(self):
                if self.heal.get() == 0:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Здоровье', 'value':'hidden'})
                else:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Здоровье', 'value':self.massiv[2]})

            def hoby_button(self):
                if self.hoby.get() == 0:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Хобби', 'value':'hidden'})
                else:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Хобби', 'value':self.massiv[3]})

            def fobia_button(self):
                if self.fobia.get() == 0:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Фобия', 'value':'hidden'})
                else:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Фобия', 'value':self.massiv[6]})

            def char_button(self):
                if self.char.get() == 0:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Характер', 'value':'hidden'})
                else:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Характер', 'value':self.massiv[4]})

            def fact_button(self):
                if self.fiact.get() == 0:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Факты', 'value':'hidden'})
                else:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Факты', 'value':self.massiv[5]})

            def bag_button(self):
                if self.bag.get() == 0:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Багаж', 'value':'hidden'})
                else:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Багаж', 'value':self.massiv[7]})

            def usl_button(self):
                if self.usl.get() == 0:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Условие', 'value':'hidden'})
                else:
                    requests.post(f'http://{server_ip}/rooms/{code}/update', json={'player':f'igrok{self.number}', 'card':'Условие', 'value':self.massiv[8]})

            # Разметка игрока
            def create(self):
                page = tk.Frame(content_frame, bg=BG_COLOR)
                # Блок Игрок 1
                page.columnconfigure(0, weight=1)
                page.columnconfigure(1, weight=3)  # Основное содержание
                page.columnconfigure(2, weight=1)
                page.rowconfigure(0, weight=1)
                page.rowconfigure(1, weight=3)     # Основное содержание  
                page.rowconfigure(2, weight=1)

                # Теперь создаем container1 и размещаем его в сетке page1
                container = tk.Frame(page, bg=BG_COLOR)
                container.grid(row=1, column=1, sticky="nsew", padx=20, pady=15)

                container.columnconfigure(0, weight=1)
                container.columnconfigure(1, weight=2)  # Центральная колонка с контентом
                container.columnconfigure(2, weight=1)
                container.columnconfigure(3, weight=0)
                container.columnconfigure(4, weight=1)

                game_code = tk.Label(container, text="🚨 КОД БУНКЕРА:", **HEADING_STYLE)
                game_code.grid(column=0,row=0,sticky='w')

                label_code = tk.Label(container,text=self.code, **HEADING_STYLE)
                label_code.grid(column=0,row=1,sticky='wn')

                for_bunker = tk.Label(container,text='В бункер хочет попасть',**HEADING_STYLE)
                for_bunker.grid(column=0,row=4,sticky='wn')

                self.count = tk.Label(container,text=f'{len(array)}/3 людей',**HEADING_STYLE)
                self.count.grid(column=0,row=5,sticky='wn')

                name = tk.Label(container, text=f"🧍 ВЫЖИВШИЙ #{self.number}", **HEADING_STYLE)
                name.grid(column=1, row=0, **PADDING)

                # Блок Профессия
                profa = tk.Label(container, text="🔧 Профессия", **HEADING_STYLE)
                profa.grid(column=1, row=1, **PADDING)

                self.profession = tk.Label(container, text=play[f"igrok{self.number}"]["Профессия"], **BUTTON_STYLE)
                self.profession.grid(column=1, row=2, **PADDING)

                # Блок Биология
                bio = tk.Label(container, text="🧬 Биология", **HEADING_STYLE)
                bio.grid(column=1, row=3, **PADDING)

                self.biology = tk.Label(container, text=play[f'igrok{self.number}']['Биология'], **BUTTON_STYLE)    
                self.biology.grid(column=1, row=4, **PADDING)

                # Блок Здоровье
                heal = tk.Label(container, text="🤧 Здоровье", **HEADING_STYLE)
                heal.grid(column=1, row=5, **PADDING)

                self.health = tk.Label(container, text=play[f'igrok{self.number}']['Здоровье'], **BUTTON_STYLE)
                self.health.grid(column=1, row=6, **PADDING)

                # Блок Хобби
                hobb = tk.Label(container, text="🎯 Хобби", **HEADING_STYLE)
                hobb.grid(column=1, row=7, **PADDING)

                self.hobby = tk.Label(container, text=play[f'igrok{self.number}']["Хобби"], **BUTTON_STYLE)
                self.hobby.grid(column=1, row=8, **PADDING)

                # Блок Фобия
                foby = tk.Label(container, text="😨 Фобия", **HEADING_STYLE)
                foby.grid(column=1, row=9, **PADDING)

                self.fobya = tk.Label(container, text=play[f'igrok{self.number}']['Фобия'], **BUTTON_STYLE)
                self.fobya.grid(column=1, row=10, **PADDING)

                # Блок Характер
                char = tk.Label(container, text="🧠 Характер", **HEADING_STYLE)
                char.grid(column=1, row=11, **PADDING)

                self.chara = tk.Label(container, text=play[f'igrok{self.number}']['Характер'], **BUTTON_STYLE)
                self.chara.grid(column=1, row=12, **PADDING)

                # Блок Факт
                facts = tk.Label(container, text="📝 Факт", **HEADING_STYLE)
                facts.grid(column=1, row=13, **PADDING)

                self.fact = tk.Label(container, text=play[f'igrok{self.number}']['Факты'], **BUTTON_STYLE)
                self.fact.grid(column=1, row=14, **PADDING)

                # Блок Багаж
                baga = tk.Label(container, text="🎒 Багаж", **HEADING_STYLE)
                baga.grid(column=1, row=15, **PADDING)

                self.bagaje = tk.Label(container, text=play[f'igrok{self.number}']['Багаж'], **BUTTON_STYLE)
                self.bagaje.grid(column=1, row=16, **PADDING)

                # Блок Условие
                usl = tk.Label(container, text="🎁 Условие", **HEADING_STYLE)
                usl.grid(column=1, row=17, **PADDING)

                self.uslovie = tk.Label(container, text=play[f'igrok{self.number}']['Условие'], **BUTTON_STYLE)
                self.uslovie.grid(column=1, row=18)

                self.chek_prof = tk.Checkbutton(container, text='', background=BG_COLOR, fg=GREEN_ACCENT, command=self.prof_button,
                                        selectcolor=BG_COLOR, activebackground=BG_COLOR, variable=self.prof)

                self.chek_bio = tk.Checkbutton(container, text='', background=BG_COLOR, fg=GREEN_ACCENT, command=self.bio_button,
                                        selectcolor=BG_COLOR, activebackground=BG_COLOR, variable=self.bio)

                self.chek_heal = tk.Checkbutton(container, text='', background=BG_COLOR, fg=GREEN_ACCENT, command=self.heal_button,
                                        selectcolor=BG_COLOR, activebackground=BG_COLOR, variable=self.heal)

                self.chek_hobby = tk.Checkbutton(container, text='', background=BG_COLOR, fg=GREEN_ACCENT, command=self.hoby_button,
                                        selectcolor=BG_COLOR, activebackground=BG_COLOR, variable=self.hoby)

                self.chek_fobya = tk.Checkbutton(container, text='', background=BG_COLOR, fg=GREEN_ACCENT, command=self.fobia_button,
                                        selectcolor=BG_COLOR, activebackground=BG_COLOR, variable=self.fobia)

                self.chek_char = tk.Checkbutton(container, text='', background=BG_COLOR, fg=GREEN_ACCENT, command=self.char_button,
                                        selectcolor=BG_COLOR, activebackground=BG_COLOR, variable=self.char)

                self.chek_fact = tk.Checkbutton(container, text='', background=BG_COLOR, fg=GREEN_ACCENT, command=self.fact_button,
                                        selectcolor=BG_COLOR, activebackground=BG_COLOR, variable=self.fiact)

                self.chek_bag = tk.Checkbutton(container, text='', background=BG_COLOR, fg=GREEN_ACCENT, command=self.bag_button,
                                        selectcolor=BG_COLOR, activebackground=BG_COLOR, variable=self.bag)

                self.chek_usl = tk.Checkbutton(container, text='', background=BG_COLOR, fg=GREEN_ACCENT, command=self.usl_button,
                                        selectcolor=BG_COLOR, activebackground=BG_COLOR, variable=self.usl)

                left_button = tk.Button(container, text='☣', font=13, fg='yellow', bg='#4A4A2A', 
                                    command=lambda:left(room_info[0][1], icon_png, icon_ico, db_path))
                left_button.grid(column=0,row=18)

                self.izgnanie = tk.Button(container, text='ИЗГНАТЬ', font=("Arial", 12, "bold"), bg=BG_COLOR, fg=RED_ACCENT,
                                relief="raised", bd=2, command=self.not_goden,width=8)
                self.izgnanie.grid(column=4,row=0,padx=(0,10))

                self.yes_or_not = tk.Label(container, text='', **ZAGOLOVOK_STYLE, fg=RED_ACCENT)
                self.yes_or_not.grid(column=1,row=19)

                question = tk.Button(container, text='❓', font=13, fg='yellow', bg='#4A4A2A',
                                command=lambda:right1(room_info[0][1], icon_png, icon_ico, db_path))
                question.grid(column=4,row=18)

                ugroza = tk.Button(container, text='⚡', font=13, fg='yellow', bg='#4A4A2A',
                                command=self.right_window)
                ugroza.grid(column=4,row=19)

                # Упаковываем page1
                page.pack(fill=tk.BOTH, expand=True)

                return page
            
            # Полное открытие всех характеристик игрока
            def characters(self):
                self.profession.config(text=self.massiv[0])
                self.biology.config(text=self.massiv[1])
                self.health.config(text=self.massiv[2])
                self.hobby.config(text=self.massiv[3])
                self.fobya.config(text=self.massiv[6])
                self.chara.config(text=self.massiv[4])
                self.fact.config(text=self.massiv[5])
                self.bagaje.config(text=self.massiv[7])
                self.uslovie.config(text=self.massiv[8])
                self.chek_prof.grid(column=2,row=2,sticky='w',padx=(0,20))
                self.chek_bio.grid(column=2,row=4,sticky='w',padx=(0,20))
                self.chek_heal.grid(column=2,row=6,sticky='w',padx=(0,20))
                self.chek_hobby.grid(column=2,row=8,sticky='w',padx=(0,20))
                self.chek_fobya.grid(column=2,row=10,sticky='w',padx=(0,20))
                self.chek_char.grid(column=2,row=12,sticky='w',padx=(0,20))
                self.chek_fact.grid(column=2,row=14,sticky='w',padx=(0,20))
                self.chek_bag.grid(column=2,row=16,sticky='w',padx=(0,20))
                self.chek_usl.grid(column=2,row=18,sticky='w',padx=(0,20))

        #Инициализация игроков и страниц
        user1 = Player(player1,1)
        user2 = Player(player2,2)
        user3 = Player(player3,3)
        user4 = Player(player4,4)
        user5 = Player(player5,5)
        user6 = Player(player6,6)
        user7 = Player(player7,7)

        page1 = user1.create()
        page2 = user2.create()
        page3 = user3.create()
        page4 = user4.create()
        page5 = user5.create()
        page6 = user6.create()
        page7 = user7.create()

        # Привязываем колесо мыши ко всем элементам внутри content_frame
        def bind_mousewheel(widget):
            if sys.platform.startswith('win'):
                widget.bind("<MouseWheel>", on_mousewheel)
            else:
                widget.bind("<Button-4>", on_mousewheel)
                widget.bind("<Button-5>", on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel(child)


        bind_mousewheel(content_frame)

        # Обновляем область прокрутки
        window.update_idletasks()
        configure_scrollregion()
        #-----------------------------------------------------------------------------
        # ФУНКЦИЯ ДЛЯ ПЕРЕКЛЮЧЕНИЯ СТРАНИЦ
        def show_page(page):
            # Сначала прячем ВСЕ страницы
            page1.pack_forget()  # прячем страницу 1
            page2.pack_forget()  # прячем страницу 2  
            page3.pack_forget()  # прячем страницу 3
            page4.pack_forget()  # прячем страницу 4
            page5.pack_forget()  # прячем страницу 5
            page6.pack_forget()  # прячем страницу 6
            page7.pack_forget()  # прячем страницу 7
            
            # Показываем только нужную страницу
            page.pack(fill="both", expand=True)  # растягиваем на всё окно

        # 3. СОЗДАЕМ КНОПКИ ДЛЯ ПЕРЕКЛЮЧЕНИЯ
        btn_frame = tk.Frame(window,bg=BG_COLOR)  # рамка для кнопок
        btn_frame.pack(side="bottom", pady=10)  # размещаем внизу

        # Стиль кнопок навигации
        NAV_BUTTON_STYLE = {
            "font": ("Arial", 10, "bold"),
            "bg": BUTTON_BG,
            "fg": ACCENT_COLOR,
            "activebackground": BUTTON_ACTIVE,
            "activeforeground": TEXT_COLOR,
            "relief": "raised",
            "bd": 2,
            "width": 10
        }

        # Кнопки страниц
        btn1 = tk.Button(btn_frame, text="Игрок 1", command=lambda: show_page(page1), **NAV_BUTTON_STYLE)
        btn1.pack(side="left", padx=5)

        btn2 = tk.Button(btn_frame, text="Игрок 2", command=lambda: show_page(page2), **NAV_BUTTON_STYLE)
        btn2.pack(side="left", padx=5)

        btn3 = tk.Button(btn_frame, text="Игрок 3", command=lambda: show_page(page3), **NAV_BUTTON_STYLE)
        btn3.pack(side="left", padx=5)

        btn4 = tk.Button(btn_frame, text="Игрок 4", command=lambda: show_page(page4), **NAV_BUTTON_STYLE)
        btn4.pack(side="left", padx=5)

        btn5 = tk.Button(btn_frame, text="Игрок 5", command=lambda: show_page(page5), **NAV_BUTTON_STYLE)
        btn5.pack(side="left", padx=5)

        btn6 = tk.Button(btn_frame, text="Игрок 6", command=lambda: show_page(page6), **NAV_BUTTON_STYLE)
        btn6.pack(side="left", padx=5)

        btn7 = tk.Button(btn_frame, text="Игрок 7", command=lambda: show_page(page7), **NAV_BUTTON_STYLE)
        btn7.pack(side="left", padx=5)

        # 4. ПОКАЗЫВАЕМ ПЕРВУЮ СТРАНИЦУ ПРИ ЗАПУСКЕ
        assoc1 = {1:page1, 2:page2, 3:page3, 4:page4, 5:page5, 6:page6, 7:page7}
        assoc2 = {1:user1, 2:user2, 3:user3, 4:user4, 5:user5, 6:user6, 7:user7}

        # Если номер игрока есть в 1 и втором словаре, показываем его, и отправляем его номер на сервер
        if player in assoc1 and player in assoc2:
            show_page(assoc1[player])
            assoc2[player].characters()
            requests.post(f'http://{server_ip}/rooms/{code}/players/accept', json={'player':player})

        # Запускаем приложение
        window.deiconify()  # Показываем окно
        # Взависимости от системы ставим полноэкранный режим
        if sys.platform.startswith('win'):
            window.state('zoomed')
        else:
            try:
                window.attributes('-zoomed', True)
            except:
                window.state('normal')

        # Однократное обновление в конце
        window.update_idletasks()
        configure_scrollregion()

        # Обновление характеристик других игроков, если они их открыли
        def sws():
            get_in = requests.get(f"http://{server_ip}/rooms/{code}")
            play = get_in.json()
            for i in range(1,8):
                assoc2[i].profession.config(text=play['play'][f'igrok{i}']['Профессия'])
                assoc2[i].biology.config(text=play['play'][f'igrok{i}']['Биология'])
                assoc2[i].health.config(text=play['play'][f'igrok{i}']['Здоровье'])
                assoc2[i].hobby.config(text=play['play'][f'igrok{i}']['Хобби'])
                assoc2[i].fobya.config(text=play['play'][f'igrok{i}']['Фобия'])
                assoc2[i].chara.config(text=play['play'][f'igrok{i}']['Характер'])
                assoc2[i].fact.config(text=play['play'][f'igrok{i}']['Факты'])
                assoc2[i].bagaje.config(text=play['play'][f'igrok{i}']['Багаж'])
                assoc2[i].uslovie.config(text=play['play'][f'igrok{i}']['Условие'])

            assoc2[player].characters()

            window.after(1000, sws)

        window.after(1000, sws)

        # Обновляем количество изгнанных игроков
        def pau():
            nonlocal array
            get_in = requests.get(f"http://{server_ip}/rooms/{code}/spisok")
            array = get_in.json()
            for i in range(1,8):
                if i not in array:
                    assoc2[i]._vikid()
            zamena()

            window.after(1000, pau)
        
        window.after(1000, pau)

        # Обработка нажатия на крестик(Закрытие)
        window.protocol("WM_DELETE_WINDOW", on_closing)

        window.mainloop()

    except sq.Error as e:
        print(f"Database error in okno4: {e}")
        import tkinter.messagebox as mb
        mb.showerror("Ошибка БД", f"Не удалось подключиться к базе данных: {e}")
        return