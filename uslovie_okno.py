import tkinter as tk
import os
import sys
import requests
import math

# Основная функция
def usl_okno(player, icon_png, icon_ico, players, code, ip, text):

    def clear_and_show(p):
        # Удаляем все виджеты из окна
        for widget in okno.winfo_children():
            widget.destroy()
        # Показываем выбор характеристики
        make_chars('one_per', p)

    def deal_char(player1, player2, char):
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
        if attr != 'Пол':
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
                    elif attr == 'Любая':
                        comanda = lambda p=player_num: clear_and_show(p)
                    elif attr == 'Запрет':
                        comanda = lambda p=player_num: (requests.post(f'http://{ip}/rooms/{code}/uslovie/zapret', json={'player':p}), okno.destroy())
                    elif attr == 'Пол':
                        comanda = lambda p=player_num: (requests.post(f'http://{ip}/rooms/{code}/uslovie/gender', json={'player':p}), okno.destroy)
                    btn = tk.Button(okno, text=player_num, **BUTTON_STYLE, command=comanda, width=3)
                    btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
                    buttons.append(btn)

                col += 1

            row += 1

    def make_chars(attr, p=None):
        title = tk.Label(okno,text="Выберите тип карты", **HEADING_STYLE)
        title.grid(column=1, row=0,columnspan=2, sticky='ew')
        if attr=='every_per': 
            chars = [
                ["🔧 Профессия",'Профессия',0],
                ["🧬 Биология",'Биология',1],
                ['🤧 Здоровье',"Здоровье",2],
                ["🎯 Хобби","Хобби",3],
                ["😨 Фобия","Фобия",4],
                ["🧠 Характер","Характер",5],
                ["📝 Факт","Факт",6],
                ["🎒 Багаж","Багаж",7]
            ]
            row = 1
            column=0
            for label, char_name, char_index in chars:
                btn = tk.Button(okno,text=label, **BUTTON_STYLE,
                command=lambda cn=char_name, ci=char_index:(requests.post(f'http://{ip}/rooms/code/uslovie/every', json={'character':cn, 'players':players, 
                'char_number':ci, 'text':text}),
                okno.destroy()))
                btn.grid(row=row, column=column, **PADDING)
                column += 1
                if column == 4:
                    column=0
                    row=2
        
        elif attr=='one_per':
            chars = [
                ["🔧 Профессия",'Профессия',0],
                ["🧬 Биология",'Биология',1],
                ['🤧 Здоровье',"Здоровье",2],
                ["🎯 Хобби","Хобби",3],
                ["😨 Фобия","Фобия",4],
                ["🧠 Характер","Характер",5],
                ["📝 Факт","Факт",6],
                ["🎒 Багаж","Багаж",7]
            ]
            row = 1
            column=0
            for label, char_name, char_index in chars:
                btn = tk.Button(okno,text=label, **BUTTON_STYLE,
                command=lambda cn=char_name, ci=char_index:(requests.post(f'http://{ip}/rooms/{code}/uslovie/open', json={'player':f'igrok{p}','character':cn,  
                'players':players, 'char_number':ci, 'text':text}),
                okno.destroy()))
                btn.grid(row=row, column=column, **PADDING)
                column += 1
                if column == 4:
                    column=0
                    row=2


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
        make_chars('every_per')

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

    elif 'любую' in text:
        make_net('Любая')
    
    elif 'Запрети' in text:
        make_net('Запрет')

    elif 'пол' in text:
        make_net('Пол')