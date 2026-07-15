import tkinter as tk
import os
import sys
import requests
import math

# Основная функция
def usl_okno(player, icon_png, icon_ico, players, code, ip, text):

    def deal_char(player1, player2, char):
        print(1)
        if char == 'профессией': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Профессия', 'text':text})
        elif char == 'здоровьем': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Здоровье', 'text':text})
        elif char == 'хобби': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Хобби', 'text':text})
        elif char == 'фобией': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Фобия', 'text':text})
        elif char == 'характером': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Характер', 'text':text})
        elif char == 'фактами': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Факты', 'text':text})
        elif char == 'багажом': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Багаж', 'text':text})
        okno.destroy()

    def make_net(attr):
        # Разбиваем игроков на строки по 4 (1-4, 5-8, 9-12)
        mesto = [[],[],[]]

        for i in range(1, len(players) + 1):
            if i <= 4:
                mesto[0].append(i)
            elif i <= 8:
                mesto[1].append(i)
            else:
                mesto[2].append(i)

        # Убираем из списков самого игрока
        for i in mesto:
            if player in i:
                i.remove(player)

        # Настраиваем 9 колонок с одинаковым весом (для центрирования)
        for i in range(9):
            okno.grid_columnconfigure(i, weight=1)

        title = tk.Label(okno, text="Выберите игрока", **HEADING_STYLE)
        title.grid(column=0, row=0, columnspan=9, sticky='ew')

        buttons = []

        # Шаблоны для 7 колонок (колонки 1-7, 0 и 8 пустые)
        # 'k' — место для кнопки, '' — пустое место
        templates = {
            1: ['', '', '', 'k', '', '', ''],
            2: ['', '', 'k', '', 'k', '', ''],
            3: ['', 'k', '', 'k', '', 'k', ''],
            4: ['k', '', 'k', '', 'k', '', 'k']
        }

        row = 1
        for group in mesto:
            if not group:
                continue

            template = templates[len(group)]
            col = 1

            for t in template:
                if t == 'k':
                    # Берём следующего игрока из группы
                    player_num = group.pop(0)

                    # Создаём команду с фиксацией значений
                    if attr == 'Поменяться':
                        comanda = lambda p1=f'igrok{player}', p2=f'igrok{player_num}', char=text.split()[1]: deal_char(p1,p2,char)
                    elif attr == 'Возраст':
                        comanda = lambda p2=player_num: (requests.post(f'http://{ip}/rooms/{code}/uslovie/age', json={'player1':player, 'player2':p2, 'text':text}), okno.destroy())
                    elif attr == 'Беременность':
                        comanda = lambda p2=player_num: (requests.post(f'http://{ip}/rooms/{code}/uslovie/child', json={'player1':player, 'player2':p2, 'text':text}), okno.destroy())

                    btn = tk.Button(okno, text=player_num, **BUTTON_STYLE, command=comanda, width=3)
                    btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
                    buttons.append(btn)

                col += 1

            row += 1

    # Цвета и стили
    BG_COLOR = "#1A1A1A"
    TEXT_COLOR = "#E0E0E0"
    ACCENT_COLOR = "#FF7B30"
    BUTTON_BG = "#2D2D2D"
    BUTTON_ACTIVE = "#CC5500"

    HEADING_STYLE = {"font": ("Arial", 16, "bold"), "bg": BG_COLOR, "fg": ACCENT_COLOR}
    BUTTON_STYLE = {"font": ("Arial", 12), "bg": BG_COLOR, "fg": TEXT_COLOR, 'height':3}
    PADDING = {"pady": 5, 'padx':(10,0)}

    # РАЗМЕТКА
    okno = tk.Toplevel()
    okno.configure(background=BG_COLOR)
    okno.geometry('535x450')
    okno.title("Окно условия")

    # Взависимости от системы ставим иконку
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


    if text=="Выбери тип карты, который должны открыть все до конца раунда":
        title = tk.Label(okno,text="Выберите тип карты", **HEADING_STYLE)
        title.grid(column=1, row=0,columnspan=2, sticky='ew')

        profession = tk.Button(okno,text="🔧 Профессия", **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Профессия', 'players':players, 'char_number':0, 'text':text}),okno.destroy()))
        profession.grid(column=0,row=1, **PADDING)

        biology = tk.Button(okno, text="🧬 Биология", **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Биология', 'players':players, 'char_number':1, 'text':text}),okno.destroy()))
        biology.grid(column=1,row=1, **PADDING)

        health = tk.Button(okno, text='🤧 Здоровье', **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Здоровье', 'players':players, 'char_number':2, 'text':text}),okno.destroy()))
        health.grid(column=2, row=1, **PADDING)

        hobby = tk.Button(okno, text='🎯 Хобби', **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Хобби', 'players':players, 'char_number':3, 'text':text}),okno.destroy()))
        hobby.grid(column=3, row=1, **PADDING)

        fobia = tk.Button(okno, text="😨 Фобия", **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Фобия', 'players':players, 'char_number':6, 'text':text}),okno.destroy()))
        fobia.grid(column=0, row=2, **PADDING)

        character = tk.Button(okno, text='🧠 Характер', **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Характер', 'players':players, 'char_number':4, 'text':text}),okno.destroy()))
        character.grid(column=1, row=2, **PADDING)

        fact = tk.Button(okno, text='📝 Факт', **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Факты', 'players':players, 'char_number':5, 'text':text}),okno.destroy()))
        fact.grid(column=2, row=2, **PADDING)

        bagaje = tk.Button(okno, text='🎒 Багаж', **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Багаж', 'players':players, 'char_number':7, 'text':text}),okno.destroy()))
        bagaje.grid(column=3, row=2, **PADDING)

    elif len(text.split()) == 2 and 'Поменяйся' in text:
        make_net('Поменяться')

    elif 'возраст' in text:
        make_net('Возраст')

    elif 'беременным' in text:
        make_net('Беременность')

    elif 'последнюю' in text:
        get_in = requests.get(f'http://{ip}/rooms/{code}/uslovie/last').json()
        print(get_in)
        okno.destroy()
        usl_okno(player, icon_png, icon_ico, players, code, ip, get_in)