import tkinter as tk
import os
import sys
import requests

# Основная функция
def usl_okno(player, icon_png, icon_ico, text, players, code, ip):

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

            