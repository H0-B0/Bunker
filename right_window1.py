import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox
import os
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def right2(code, icon_png, icon_ico, db_path):
    
    # Используй переданный db_path!
    with sq.connect(db_path) as dannie:  # ← ВАЖНО: используй db_path
        cur = dannie.cursor()
        cur.execute("SELECT ugroza FROM rooms WHERE code = ?",(code,))
        data = cur.fetchall()[0][0].split(';')

    def baton():
        zagolovok.config(text=f'{data[0]}')
        trouble.config(text=f'{data[1]}')
        should.config(text=f'{data[2]}')
        batonhcik.destroy()

    # Стиль апокалипсиса
    BG_COLOR = "#1A1A1A"  # Тёмно-серый, почти чёрный
    TEXT_COLOR = "#E0E0E0"  # Светло-серый
    ACCENT_COLOR = "#FF7B30"  # Ржавый оранжевый
    BUTTON_BG = "#2D2D2D"  # Тёмно-серый для кнопок
    BUTTON_ACTIVE = "#CC5500"  # Тёмно-оранжевый при нажатии
    
    ZAGOLOVOK_STYLE = {"font": ("Arial", 12, "bold"), "bg": BG_COLOR, 'fg':ACCENT_COLOR}
    BUTTON_STYLE = {"font": ("Arial", 12), "bg": BG_COLOR, 'fg' : TEXT_COLOR}
    STYLE = {"font": ("Arial", 12), "bg": BG_COLOR, 'fg' : 'red'}

    okno = tk.Toplevel()
    okno.configure(background=BG_COLOR)
    okno.geometry('450x700')
    if sys.platform.startswith('win'):
        if icon_ico and os.path.exists(icon_ico):
            okno.iconbitmap(icon_ico)
    else:
        if icon_png and os.path.exists(icon_png):
            try:
                img = tk.PhotoImage(file=icon_png)
                okno.iconphoto(True, img)
            except: pass

    zagolovok = tk.Label(okno,text='',**ZAGOLOVOK_STYLE,wraplength=150)
    zagolovok.grid(column=0,row=0,padx=(70,0))

    trouble = tk.Label(okno,text='',**BUTTON_STYLE,wraplength=150)
    trouble.grid(column=0,row=1,padx=(40,0),pady=(20,0))

    should = tk.Label(okno,text='',**BUTTON_STYLE,wraplength=150)
    should.grid(column=0,row=2,padx=(70,0),pady=(20,0))

    batonhcik = tk.Button(okno, text='Открыть концовку',command=baton,**STYLE)
    batonhcik.grid(column=0,row=3,pady=(120,0),padx=(90,0))

    must = tk.Label(okno,text='Не нажимайте, пока ведущий не разрешит!!!',**ZAGOLOVOK_STYLE)
    must.grid(column=0,row=4,pady=(100,0),padx=(60,0))

if __name__ == '__main__':
    right2('25Y')