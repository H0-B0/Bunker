import tkinter as tk
import os
import sys
import requests
import math

# Основная функция
def usl_okno(player, icon_png, icon_ico, players, code, ip, text):

    def deal_char(player1, player2, char):
        print(1)
        if char == 'профессией': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Профессия'})
        elif char == 'здоровьем': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Здоровье'})
        elif char == 'хобби': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Хобби'})
        elif char == 'фобией': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Фобия'})
        elif char == 'характером': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Характер'})
        elif char == 'фактами': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Факты'})
        elif char == 'багажом': requests.post(f'http://{ip}/rooms/{code}/uslovie/char', json={'player1':player1, 'player2':player2, 'char':'Багаж'})
        okno.destroy()

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
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Профессия', 'players':players, 'char_number':0}),okno.destroy()))
        profession.grid(column=0,row=1, **PADDING)

        biology = tk.Button(okno, text="🧬 Биология", **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Биология', 'players':players, 'char_number':1}),okno.destroy()))
        biology.grid(column=1,row=1, **PADDING)

        health = tk.Button(okno, text='🤧 Здоровье', **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Здоровье', 'players':players, 'char_number':2}),okno.destroy()))
        health.grid(column=2, row=1, **PADDING)

        hobby = tk.Button(okno, text='🎯 Хобби', **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Хобби', 'players':players, 'char_number':3}),okno.destroy()))
        hobby.grid(column=3, row=1, **PADDING)

        fobia = tk.Button(okno, text="😨 Фобия", **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Фобия', 'players':players, 'char_number':6}),okno.destroy()))
        fobia.grid(column=0, row=2, **PADDING)

        character = tk.Button(okno, text='🧠 Характер', **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Характер', 'players':players, 'char_number':4}),okno.destroy()))
        character.grid(column=1, row=2, **PADDING)

        fact = tk.Button(okno, text='📝 Факт', **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Факты', 'players':players, 'char_number':5}),okno.destroy()))
        fact.grid(column=2, row=2, **PADDING)

        bagaje = tk.Button(okno, text='🎒 Багаж', **BUTTON_STYLE
        ,command=lambda:(requests.post(f'http://{ip}/rooms/{code}/uslovie/every', json={'character':'Багаж', 'players':players, 'char_number':7}),okno.destroy()))
        bagaje.grid(column=3, row=2, **PADDING)

    elif len(text.split()) == 2 and 'Поменяйся' in text:
        # Разбиваем игроков на строки по 4 (1-4, 5-8, 9-12)
        mesto = [[],[],[]]

        for i in range(1,len(players)+1):
            if i <= 4:
                mesto[0].append(i)
            elif i <= 8:
                mesto[1].append(i)
            else: mesto[2].append(i)

        # Убираем из списков самого игрока
        for i in mesto:
            if player in i:
                i.remove(player)
        
        # Настраиваем 9 колонок с одинаковым весом (для центрирования)
        for i in range(9):
            okno.grid_columnconfigure(i, weight=1)

        title = tk.Label(okno,text="Выберите игрока", **HEADING_STYLE)
        title.grid(column=0, row=0,columnspan=9, sticky='ew')

        buttons = []

        index = 0 # Текущий индекс в место
        play_index = 0 # Индекс номера

        # Шаблоны для 7 колонок (колонки 1-7, 0 и 8 пустые)
        # 'k' — место для кнопки, '' — пустое место
        one = ['','','','k','','','']
        two = ['','','k','','k','','',]
        three = ['','k','','k','','k','']
        four = ['k','','k','','k','','k']

        # Проходим по строкам (максимум 3 строки, т.к. игроков <= 10)
        for row in range(0,math.ceil(len(players)/4)):
            print(len(mesto[index]))
            if len(mesto[index]) == 1:
                column = 1 # Начинаем с первой колонки(0 и 8 пустые)
                play_index = 0
                for col in one:
                    print(index,play_index)
                    if col == 'k': # Только если при переборе будет k, то ставим кнопку
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p1=f'igrok{player}', p2=f'igrok{mesto[index][play_index]}', char=text.split()[1]: deal_char(p1,p2,char), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                    column += 1
                    print(index,play_index)
            elif len(mesto[index]) == 2:
                print(index,play_index)
                column = 1
                play_index = 0
                for col in two:
                    if col == 'k':
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p1=f'igrok{player}', p2=f'igrok{mesto[index][play_index]}', char=text.split()[1]: deal_char(p1,p2,char), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                        play_index += 1
                    column += 1
            elif len(mesto[index]) == 3:
                print(index,play_index)
                column = 1
                play_index = 0
                for col in three:
                    if col == 'k':
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p1=f'igrok{player}', p2=f'igrok{mesto[index][play_index]}', char=text.split()[1]: deal_char(p1,p2,char), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                        play_index += 1
                    column += 1
            elif len(mesto[index]) == 4:
                print(index,play_index)
                column = 1
                play_index = 0
                for col in four:
                    if col == 'k':
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p1=f'igrok{player}', p2=f'igrok{mesto[index][play_index]}', char=text.split()[1]: deal_char(p1,p2,char), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                        play_index += 1
                    column += 1
            else:
                continue
            index += 1
            if index > 3: break # Если больше 3 строки, то стопаем

    elif 'возраст' in text:
        # Разбиваем игроков на строки по 4 (1-4, 5-8, 9-12)
        mesto = [[],[],[]]

        for i in range(1,len(players)+1):
            if i <= 4:
                mesto[0].append(i)
            elif i <= 8:
                mesto[1].append(i)
            else: mesto[2].append(i)

        # Убираем из списков самого игрока
        for i in mesto:
            if player in i:
                i.remove(player)
        
        # Настраиваем 9 колонок с одинаковым весом (для центрирования)
        for i in range(9):
            okno.grid_columnconfigure(i, weight=1)

        title = tk.Label(okno,text="Выберите игрока", **HEADING_STYLE)
        title.grid(column=0, row=0,columnspan=9, sticky='ew')

        buttons = []

        index = 0 # Текущий индекс в место
        play_index = 0 # Индекс номера

        # Шаблоны для 7 колонок (колонки 1-7, 0 и 8 пустые)
        # 'k' — место для кнопки, '' — пустое место
        one = ['','','','k','','','']
        two = ['','','k','','k','','',]
        three = ['','k','','k','','k','']
        four = ['k','','k','','k','','k']

        # Проходим по строкам (максимум 3 строки, т.к. игроков <= 10)
        for row in range(0,math.ceil(len(players)/4)):
            print(len(mesto[index]))
            if len(mesto[index]) == 1:
                column = 1 # Начинаем с первой колонки(0 и 8 пустые)
                play_index = 0
                for col in one:
                    print(index,play_index)
                    if col == 'k': # Только если при переборе будет k, то ставим кнопку
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/age', json={'player1':player, 'player2':p2})), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                    column += 1
                    print(index,play_index)
            elif len(mesto[index]) == 2:
                print(index,play_index)
                column = 1
                play_index = 0
                for col in two:
                    if col == 'k':
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/age', json={'player1':player, 'player2':p2})), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                        play_index += 1
                    column += 1
            elif len(mesto[index]) == 3:
                print(index,play_index)
                column = 1
                play_index = 0
                for col in three:
                    if col == 'k':
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/age', json={'player1':player, 'player2':p2})), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                        play_index += 1
                    column += 1
            elif len(mesto[index]) == 4:
                print(index,play_index)
                column = 1
                play_index = 0
                for col in four:
                    if col == 'k':
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/age', json={'player1':player, 'player2':p2})), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                        play_index += 1
                    column += 1
            else:
                continue
            index += 1
            if index > 3: break # Если больше 3 строки, то стопаем

    elif 'беременным' in text:
        # Разбиваем игроков на строки по 4 (1-4, 5-8, 9-12)
        mesto = [[],[],[]]

        for i in range(1,len(players)+1):
            if i <= 4:
                mesto[0].append(i)
            elif i <= 8:
                mesto[1].append(i)
            else: mesto[2].append(i)

        # Убираем из списков самого игрока
        for i in mesto:
            if player in i:
                i.remove(player)
        
        # Настраиваем 9 колонок с одинаковым весом (для центрирования)
        for i in range(9):
            okno.grid_columnconfigure(i, weight=1)

        title = tk.Label(okno,text="Выберите игрока", **HEADING_STYLE)
        title.grid(column=0, row=0,columnspan=9, sticky='ew')

        buttons = []

        index = 0 # Текущий индекс в место
        play_index = 0 # Индекс номера

        # Шаблоны для 7 колонок (колонки 1-7, 0 и 8 пустые)
        # 'k' — место для кнопки, '' — пустое место
        one = ['','','','k','','','']
        two = ['','','k','','k','','',]
        three = ['','k','','k','','k','']
        four = ['k','','k','','k','','k']

        # Проходим по строкам (максимум 3 строки, т.к. игроков <= 10)
        for row in range(0,math.ceil(len(players)/4)):
            print(len(mesto[index]))
            if len(mesto[index]) == 1:
                column = 1 # Начинаем с первой колонки(0 и 8 пустые)
                play_index = 0
                for col in one:
                    print(index,play_index)
                    if col == 'k': # Только если при переборе будет k, то ставим кнопку
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/child', json={'player1':player, 'player2':p2})), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                    column += 1
                    print(index,play_index)
            elif len(mesto[index]) == 2:
                print(index,play_index)
                column = 1
                play_index = 0
                for col in two:
                    if col == 'k':
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/child', json={'player1':player, 'player2':p2})), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                        play_index += 1
                    column += 1
            elif len(mesto[index]) == 3:
                print(index,play_index)
                column = 1
                play_index = 0
                for col in three:
                    if col == 'k':
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/child', json={'player1':player, 'player2':p2})), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                        play_index += 1
                    column += 1
            elif len(mesto[index]) == 4:
                print(index,play_index)
                column = 1
                play_index = 0
                for col in four:
                    if col == 'k':
                        buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                        command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/child', json={'player1':player, 'player2':p2})), width=3))
                        buttons[-1].grid(column=column, row=row+1, sticky='ew')
                        play_index += 1
                    column += 1
            else:
                continue
            index += 1
            if index > 3: break # Если больше 3 строки, то стопаем

    elif 'беременным' in text:
        # Разбиваем игроков на строки по 4 (1-4, 5-8, 9-12)
            mesto = [[],[],[]]

            for i in range(1,len(players)+1):
                if i <= 4:
                    mesto[0].append(i)
                elif i <= 8:
                    mesto[1].append(i)
                else: mesto[2].append(i)

            # Убираем из списков самого игрока
            for i in mesto:
                if player in i:
                    i.remove(player)
            
            # Настраиваем 9 колонок с одинаковым весом (для центрирования)
            for i in range(9):
                okno.grid_columnconfigure(i, weight=1)

            title = tk.Label(okno,text="Выберите игрока", **HEADING_STYLE)
            title.grid(column=0, row=0,columnspan=9, sticky='ew')

            buttons = []

            index = 0 # Текущий индекс в место
            play_index = 0 # Индекс номера

            # Шаблоны для 7 колонок (колонки 1-7, 0 и 8 пустые)
            # 'k' — место для кнопки, '' — пустое место
            one = ['','','','k','','','']
            two = ['','','k','','k','','',]
            three = ['','k','','k','','k','']
            four = ['k','','k','','k','','k']

            # Проходим по строкам (максимум 3 строки, т.к. игроков <= 10)
            for row in range(0,math.ceil(len(players)/4)):
                print(len(mesto[index]))
                if len(mesto[index]) == 1:
                    column = 1 # Начинаем с первой колонки(0 и 8 пустые)
                    play_index = 0
                    for col in one:
                        print(index,play_index)
                        if col == 'k': # Только если при переборе будет k, то ставим кнопку
                            buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                            command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/child', json={'player1':player, 'player2':p2}), okno.destroy()), width=3))
                            buttons[-1].grid(column=column, row=row+1, sticky='ew')
                        column += 1
                        print(index,play_index)
                elif len(mesto[index]) == 2:
                    print(index,play_index)
                    column = 1
                    play_index = 0
                    for col in two:
                        if col == 'k':
                            buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                            command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/child', json={'player1':player, 'player2':p2}), okno.destroy()), width=3))
                            buttons[-1].grid(column=column, row=row+1, sticky='ew')
                            play_index += 1
                        column += 1
                elif len(mesto[index]) == 3:
                    print(index,play_index)
                    column = 1
                    play_index = 0
                    for col in three:
                        if col == 'k':
                            buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                            command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/child', json={'player1':player, 'player2':p2}), okno.destroy()), width=3))
                            buttons[-1].grid(column=column, row=row+1, sticky='ew')
                            play_index += 1
                        column += 1
                elif len(mesto[index]) == 4:
                    print(index,play_index)
                    column = 1
                    play_index = 0
                    for col in four:
                        if col == 'k':
                            buttons.append(tk.Button(okno, text=mesto[index][play_index], **BUTTON_STYLE, 
                            command=lambda p2=mesto[index][play_index]:(requests.post(f'http://{ip}/rooms/{code}/uslovie/child', json={'player1':player, 'player2':p2}), okno.destroy()), width=3))
                            buttons[-1].grid(column=column, row=row+1, sticky='ew')
                            play_index += 1
                        column += 1
                else:
                    continue
                index += 1
                if index > 3: break # Если больше 3 строки, то стопаем