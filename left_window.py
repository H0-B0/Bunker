import tkinter as tk
import sqlite3 as sq
import os
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def left(code, icon_png, icon_ico, db_path):
    with sq.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT kard, flats, apoc, years, mesto, ploshad FROM rooms WHERE code = ?", (code,))
        data = cur.fetchall()

    tools = data[0][0]
    rooms = data[0][1]
    apocalypsys = data[0][2].split(';')
    year = data[0][3]
    mesto = data[0][4]
    s = data[0][5]

    BG_COLOR = "#1A1A1A"
    TEXT_COLOR = "#E0E0E0"
    ACCENT_COLOR = "#FF7B30"
    BUTTON_BG = "#2D2D2D"
    BUTTON_ACTIVE = "#CC5500"

    HEADING_STYLE = {"font": ("Arial", 16, "bold"), "bg": BG_COLOR, "fg": ACCENT_COLOR}
    BUTTON_STYLE = {"font": ("Arial", 12), "bg": BG_COLOR, "fg": TEXT_COLOR}
    PADDING = {"pady": 5}

    okno = tk.Toplevel()
    okno.configure(background=BG_COLOR)
    okno.geometry('650x400')
    okno.title("Информация о бункере")

    # Иконка
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

    # ========== ПРОКРУТКА (bind_all) ==========
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
        # Показать/скрыть скроллбар в зависимости от высоты контента
        bbox = canvas.bbox("all")
        if bbox and bbox[3] > okno.winfo_height():
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
            # Linux: определяем по event.num (4 - вверх, 5 - вниз)
            if event.num == 4:
                delta = -1
            elif event.num == 5:
                delta = 1
            else:
                delta = 0
        if delta != 0:
            canvas.yview_scroll(delta, "units")
        return "break"

    # Глобальная привязка ко всем окнам (включая дочерние)
    if sys.platform.startswith('win'):
        okno.bind_all("<MouseWheel>", on_mousewheel)
    else:
        okno.bind_all("<Button-4>", on_mousewheel)
        okno.bind_all("<Button-5>", on_mousewheel)

    content_frame.bind("<Configure>", configure_scrollregion)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=canvas.winfo_width()))

    # Упаковываем canvas (скроллбар появится/исчезнет в configure_scrollregion)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    okno.bind("<Configure>", lambda e: configure_scrollregion())
    # ========== КОНЕЦ ПРОКРУТКИ ==========

    # Контент (без изменений)
    apoc_title = tk.Label(content_frame, text='Апокалипсис:', **HEADING_STYLE)
    apoc_title.grid(column=0, row=0, sticky='w', padx=20)

    apoc = tk.Label(content_frame, text=apocalypsys[0], **HEADING_STYLE)
    apoc.grid(column=1, row=0, padx=(50,20), sticky='we')

    apoc_text = tk.Label(content_frame, text=apocalypsys[1], **BUTTON_STYLE, wraplength=300, **PADDING)
    apoc_text.grid(column=1, row=1, padx=(50,20), sticky='w')

    separator1 = tk.Frame(content_frame, height=2, bg=ACCENT_COLOR)
    separator1.grid(column=0, columnspan=2, row=2, sticky='we', padx=20, pady=10)

    tools_title = tk.Label(content_frame, text='В бункере есть:', **HEADING_STYLE)
    tools_title.grid(column=0, row=3, pady=(0,0), sticky='nw', padx=20)

    tools_text = tk.Label(content_frame, text=tools.replace(',', '\n\n'), **BUTTON_STYLE, wraplength=300)
    tools_text.grid(column=1, row=3, padx=(50,20), pady=(0,0), sticky='w')

    separator2 = tk.Frame(content_frame, height=2, bg=ACCENT_COLOR)
    separator2.grid(column=0, columnspan=2, row=4, sticky='we', padx=20, pady=10)

    rooms_title = tk.Label(content_frame, text='Помещения в бункере:', **HEADING_STYLE)
    rooms_title.grid(column=0, row=5, pady=(0,0), sticky='nw', padx=20)

    rooms_text = tk.Label(content_frame, text=rooms.replace(';', '\n\n'), **BUTTON_STYLE, wraplength=300)
    rooms_text.grid(column=1, row=5, pady=(0,0), padx=(50,20), sticky='w')

    separator3 = tk.Frame(content_frame, height=2, bg=ACCENT_COLOR)
    separator3.grid(column=0, columnspan=2, row=6, sticky='we', padx=20, pady=10)

    years = tk.Label(content_frame, text=f'В бункере на {year} лет', **BUTTON_STYLE)
    years.grid(column=1, row=7, pady=(0,0), padx=(50,20), sticky='w')

    separator4 = tk.Frame(content_frame, height=2, bg=ACCENT_COLOR)
    separator4.grid(column=0, columnspan=2, row=8, sticky='we', padx=20, pady=10)

    place = tk.Label(content_frame, text="Бункер расположен в ", **HEADING_STYLE)
    place.grid(column=0, row=9, pady=(0,0), padx=20, sticky='w')

    raspolozhenie = tk.Label(content_frame, text=mesto, **BUTTON_STYLE)
    raspolozhenie.grid(column=1, row=9, pady=(0,0), padx=(50,20), sticky='w')

    separator5 = tk.Frame(content_frame, height=2, bg=ACCENT_COLOR)
    separator5.grid(column=0, columnspan=2, row=10, sticky='we', padx=20, pady=10)

    ploshad = tk.Label(content_frame, text=f'Площадь бункера - {s}м^2', **BUTTON_STYLE)
    ploshad.grid(column=1, row=11, pady=(0,0), padx=(50,20), sticky='w')

    bottom_padding = tk.Frame(content_frame, height=20, bg=BG_COLOR)
    bottom_padding.grid(column=0, columnspan=2, row=12)

    okno.update_idletasks()
    configure_scrollregion()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    left('DMA', 'bunker.png', 'bunker.ico', 'base.db')
    root.mainloop()