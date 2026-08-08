import tkinter as tk
import random as r
import sqlite3 as sq
from left_window import left
from right_window1 import right2
from right_window2 import right1
from uslovie_okno import usl_okno
import os
import sys
from tkinter.messagebox import showerror
import requests
import math
from functools import partial
import asyncio
import websockets
import threading
import json

# Нааходим БД и картинки
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#Основная функция
def game_okno(player, icon_png, icon_ico, db_path, max_p, code='', server_ip='127.0.0.1:8000'):
    
    print(f"okno4: db_path = {db_path}")
    print(f"okno4: db exists = {os.path.exists(db_path) if db_path else False}")
    print(f"okno4: server_ip = {server_ip}")
    try:
        #Если код комнаты пустой(То есть она создается), то берем рандомную по количеству игроков и извлекаем из нее данные
        with sq.connect(db_path) as dannie:
            cur = dannie.cursor()
            if code == '':
                cur.execute(f'''
                    SELECT room_id FROM (
                        SELECT room_id, COUNT(player_id) as player_count
                        FROM svazka
                        GROUP BY room_id
                        HAVING COUNT(player_id) = {max_p}
                    )
                    ORDER BY RANDOM()
                    LIMIT 1
                ''')

                id_room = cur.fetchall()
                # Нужно для того, чтобы выделить случайную комнату в которой есть 4 игрока

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

        # Список игроков и начальных данных
        play = {}
        locks = {}
        voices = {}
        for i in range(1,max_p+1):
            play[f"igrok{i}"] = {
    "Профессия":"hidden",
    "Биология":"hidden",
    "Здоровье":"hidden",
    "Хобби":"hidden",
    "Фобия":"hidden",
    "Характер":"hidden",
    "Факты":"hidden",
    "Багаж":"hidden",
    "Условие":"hidden"}
            locks[f'igrok{i}'] = ''
            voices[i] = 0

        #Закидываем на сервер информацию о игроках
        requests.post(f'http://{server_ip}/rooms/{code}', json={'play':play})

        #Закидываем локи на сервер
        requests.post(f'http://{server_ip}/rooms/{code}/locks', json={'locks':locks})

        #Закидываем изначальные голоса на сервер
        requests.post(f'http://{server_ip}/rooms/{code}/voicess', json={'play':voices})

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
        IZGON_STYLE = {"font": ("Arial", 12, "bold"), "fg": ACCENT_COLOR}
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
        array = []
        for i in range(1,max_p+1): array.append(i)
        requests.post(f'http://{server_ip}/rooms/{code}/spisok', json={'array':array})

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

        async def listener():
            nonlocal player
            nonlocal array
            nonlocal last
            nonlocal locks
            nonlocal golosa
            nonlocal voices

            async with websockets.connect(f'ws://{server_ip}/ws/{code}') as ws:
                while True:
                    raw = await ws.recv()

                    try:
                        text = json.loads(raw)
                    except json.JSONDecodeError:
                        if raw == 'ping':
                            await ws.send('pong')
                            print('pong')
                        else:
                            print(raw)
                        continue
                            
                    print(text)

                    for msg in text:
                        print(f'Сейчас {msg}')
                        if msg == 'voices':
                            golosa = requests.get(f'http://{server_ip}/rooms/{code}/igroks').json()

                            voices = requests.get(f'http://{server_ip}/rooms/{code}/voice_p').json()
                            voice_keys = list(map(int,voices.keys()))
                            voice_values = list(voices.values())
                
                            new_voices = {}
                
                            # Заполняем новое голсование и обновляем таблицу голосвания
                            for key, value in zip(voice_keys, voice_values):
                                new_voices[key] = value
                            voices = new_voices
                
                            for user in users:
                                for i in voice_keys:
                                    users[user].igroks[i-1].config(text=voices[i])
                
                                # Если хотя бы кто-то за кого-то проголосовал, то открывется окно голосования
                                if any(s in [1,2,3,4,5,6,7,8,9] for s in voice_values):
                                    users[user].vote_frame.grid(row=6, column=0, rowspan=11, sticky="new", pady=10)
                                    if last == 0:
                                        users[user].kolVo_golosov.config(text=f'{golosa} из {len(array)}')
                                    elif last > 1:
                                        users[user].kolVo_golosov.config(text=f'{golosa} из {len(array)+1}')
                                else:
                                    users[user].vote_frame.grid_forget()
                
                                # Если 0, то пропускаем, а если пустая строка, то значит игрок изгнан
                                for voice in range(len(voice_values)):
                                    if voice_values[voice] == 0:
                                        continue
                                    elif voice_values[voice] == '':
                                        users[user].igroks[voice].config(text='Изгнан')

                        elif msg == 'main':
                            # Обновление характеристик других игроков, если они их открыли
                            play = requests.get(f"http://{server_ip}/rooms/{code}").json()
                            print(play)
                            if play[f'igrok{player}']['Профессия'] != 'hidden': users[player].massiv[0] = play[f'igrok{player}']['Профессия']
                            if play[f'igrok{player}']['Биология'] != 'hidden': users[player].massiv[1] = play[f'igrok{player}']['Биология']
                            if play[f'igrok{player}']['Здоровье'] != 'hidden': users[player].massiv[2] = play[f'igrok{player}']['Здоровье']
                            if play[f'igrok{player}']['Хобби'] != 'hidden': users[player].massiv[3] = play[f'igrok{player}']['Хобби']
                            if play[f'igrok{player}']['Фобия'] != 'hidden': users[player].massiv[6] = play[f'igrok{player}']['Фобия']
                            if play[f'igrok{player}']['Характер'] != 'hidden': users[player].massiv[4] = play[f'igrok{player}']['Характер']
                            if play[f'igrok{player}']['Факты'] != 'hidden': users[player].massiv[5] = play[f'igrok{player}']['Факты']
                            if play[f'igrok{player}']['Багаж'] != 'hidden': users[player].massiv[7] = play[f'igrok{player}']['Багаж']
                            for i in range(1,max_p+1):
                                users[i].profession.config(text=play[f'igrok{i}']['Профессия'])
                                users[i].biology.config(text=play[f'igrok{i}']['Биология'])
                                users[i].health.config(text=play[f'igrok{i}']['Здоровье'])
                                users[i].hobby.config(text=play[f'igrok{i}']['Хобби'])
                                users[i].fobya.config(text=play[f'igrok{i}']['Фобия'])
                                users[i].chara.config(text=play[f'igrok{i}']['Характер'])
                                users[i].fact.config(text=play[f'igrok{i}']['Факты'])
                                users[i].bagaje.config(text=play[f'igrok{i}']['Багаж'])
                                users[i].uslovie.config(text=play[f'igrok{i}']['Условие'])
                                users[i]
                            users[player].characters()

                        elif msg == 'array':
                            # Сверка старого количества игроков с новым, и удаление возможности голосования у того, кто был изгнан предыдущим, если кого-то изгнали до этого
                            get_in = requests.get(f"http://{server_ip}/rooms/{code}/spisok").json()
                            if len(get_in)<len(array):
                                print(get_in)
                                for i in range(1,max_p+1):
                                    users[i].izgnanie.config(text='ПРОГОЛОСОВАТЬ',fg=RED_ACCENT)
                                    if i not in get_in and i != last and last > 0:
                                        users[i]._vikid()
                                        users[i].real_izgoy()
                                    elif i not in get_in:
                                        users[i]._vikid()
                            array = get_in
                
                            zamena()

                        elif msg == 'locks':
                            #Если была использована карта условия на открытие или изменение характеристики, то с помощью локс у характеристики пропадет чекбокс в функции del_check
                            get_locks = requests.get(f'http://{server_ip}/rooms/{code}/uslovie/locks').json()
                            for i in range(1,max_p+1):
                                users[i].del_check(get_locks[f'igrok{i}'])

                        elif msg == 'last':
                            # В ласт записывается последний изгнанный игрок, чтобы он мог голосовать
                            last = requests.get(f'http://{server_ip}/rooms/{code}/last').json()
                

        # Функция меняющая количество игроков
        def zamena():
            for i in range(1,max_p+1):
                users[i].count.config(text=f'{len(array)}/{math.floor(max_p/2)} людей')

        # Функция убирающая игрока, если окно закрывается
        def on_closing():
            # try для того, чтобы если сервер выключен, можно было закрыть окно
            try:
                requests.post(f'http://{server_ip}/rooms/{code}/players/del', json={'player':player})
            except Exception:
                window.destroy()
            window.destroy()

        last = 0

        golosa = 0

        players_now = len(play)

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

                # Массив для заполнения окна голосования игроками
                self.igroks = []

            def del_check(self,char):
                if char == {}:
                    pass
                else:
                    if char == 'Профессия': self.chek_prof.grid_forget()
                    elif char == 'Биология': self.chek_bio.grid_forget()
                    elif char == "Здоровье": self.chek_heal.grid_forget()
                    elif char == 'Хобби': self.chek_hobby.grid_forget()
                    elif char == 'Фобия': self.chek_fobya.grid_forget()
                    elif char == 'Характер': self.chek_char.grid_forget()
                    elif char == 'Факты': self.chek_fact.grid_forget()
                    elif char == 'Багаж': self.chek_bag.grid_forget()
                    elif char == 'Условие': self.chek_usl.grid_forget()

            # ФУНКЦИИ КНОПОК
            def right_window(self):
                if len(array) != math.floor(max_p/2):
                    showerror(title='Ошибка',message=f'Чтобы открыть угрозу в комнате должно остаться {math.floor(max_p/2)} игрока')
                else:
                    right2(room_info[0][1], icon_png, icon_ico, db_path)

            def not_goden(self):
                hz = self.izgnanie.cget('text')
                if hz == 'ПРОГОЛОСОВАТЬ':
                    self.izgnanie.config(text='УБРАТЬ ГОЛОС',fg="#00E400")
                    usl_okno(player, icon_png, icon_ico, players, code, server_ip,'Убрать игрока', array)
                elif hz == 'УБРАТЬ ГОЛОС':
                    self.izgnanie.config(text='ПРОГОЛОСОВАТЬ',fg=RED_ACCENT)
                    requests.post(f'http://{server_ip}/rooms/{code}/voice_d', json={'player':self.number})

            def real_izgoy(self):
                self.izgnanie.grid_forget()

            def activate_usl(self):
                self.chek_usl.grid_forget()
                self.act_usl.grid_forget()
                usl_okno(player, icon_png, icon_ico, players, code, server_ip,self.uslovie.cget('text'), array)

            def _vikid(self):
                self.yes_or_not.config(text='НЕ ГОДЕН', fg=RED_ACCENT)

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
                    self.act_usl.grid(column=0,row=18,sticky='e')

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

                # ========== ФРЕЙМ ГОЛОСОВАНИЯ (СЛЕВА, ПО ЦЕНТРУ) ==========

                VOTE_BG = "#2A2A2A"  # Чуть светлее основного фона

                self.vote_frame = tk.Frame(container, bg=VOTE_BG, relief="ridge", bd=2, width=150)

                # Строки для игроков (7 строк)
                for i in range(1, len(play)+1):

                    lbl = tk.Label(self.vote_frame, text=f"Игрок {i}", **IZGON_STYLE, bg=VOTE_BG)
                    lbl.grid(row=i, column=0, sticky='w', padx=10, pady=5)

                    igrok = tk.Label(self.vote_frame, text=list(voices.values())[i-1], **IZGON_STYLE, bg=VOTE_BG)
                    self.igroks.append(igrok)
                    igrok.grid(row=i, column=1, sticky='e', pady=5)

                self.kolVo_golosov = tk.Label(self.vote_frame, text=f'{golosa} из {players_now}', **IZGON_STYLE, bg=VOTE_BG)
                self.kolVo_golosov.grid(row=len(play)+1, column=0, pady=5)

                # ===========================================================

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

                self.count = tk.Label(container,text=f'{len(array)}/{math.floor(max_p/2)} людей',**HEADING_STYLE)
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
                
                self.act_usl = tk.Button(container, text='Активировать условие', background='#4A4A2A', font=13,fg='yellow', command=self.activate_usl)

                left_button = tk.Button(container, text='☣', font=13, fg='yellow', bg='#4A4A2A', 
                                    command=lambda:left(room_info[0][1], icon_png, icon_ico, db_path))
                left_button.grid(column=0,row=19)

                self.izgnanie = tk.Button(container, text='ПРОГОЛОСОВАТЬ', font=("Arial", 12, "bold"), bg=BG_COLOR, fg=RED_ACCENT,
                                relief="raised", bd=2, command=self.not_goden,width=16)

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

            def checks(self):
                self.chek_prof.grid(column=2,row=2,sticky='w',padx=(0,20))
                self.chek_bio.grid(column=2,row=4,sticky='w',padx=(0,20))
                self.chek_heal.grid(column=2,row=6,sticky='w',padx=(0,20))
                self.chek_hobby.grid(column=2,row=8,sticky='w',padx=(0,20))
                self.chek_fobya.grid(column=2,row=10,sticky='w',padx=(0,20))
                self.chek_char.grid(column=2,row=12,sticky='w',padx=(0,20))
                self.chek_fact.grid(column=2,row=14,sticky='w',padx=(0,20))
                self.chek_bag.grid(column=2,row=16,sticky='w',padx=(0,20))
                self.chek_usl.grid(column=2,row=18,sticky='w',padx=(0,20))
                self.izgnanie.grid(column=4,row=0,padx=(0,10))

        #Инициализация игроков и страниц
        users = {}
        pages = {}
        for i in range(1,max_p+1):
            users[i] = Player(players[i-1],i)
            pages[i] = users[i].create()

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
            for i in range(1,max_p+1):pages[i].pack_forget()
            
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
        btns = {}
        for i in range(1,max_p+1):
            btns[i] = tk.Button(btn_frame, text=f"Игрок {i}", command=partial(show_page, pages[i]), **NAV_BUTTON_STYLE)
            btns[i].pack(side='left', padx=5)

        # 4. ПОКАЗЫВАЕМ ПЕРВУЮ СТРАНИЦУ ПРИ ЗАПУСКE
        show_page(pages[player])
        users[player].characters()
        users[player].checks()
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

        # Обработка нажатия на крестик(Закрытие)
        window.protocol("WM_DELETE_WINDOW", on_closing)

# Почему-то без этого, слушатель не работает
###############################################################
        def run_ws():
            asyncio.run(listener())

        ws_tread = threading.Thread(target=run_ws, daemon=True)
        ws_tread.start()
###############################################################

        window.mainloop()

    except sq.Error as e:
        print(f"Database error in okno4: {e}")
        import tkinter.messagebox as mb
        mb.showerror("Ошибка БД", f"Не удалось подключиться к базе данных: {e}")
        return