import tkinter as tk
import os
import sys

###
#У этого окна минимальная значимость
###
def rules(icon_png, icon_ico, db_path):
    # Стиль апокалипсиса
    BG_COLOR = "#1A1A1A"  # Тёмно-серый, почти чёрный
    TEXT_COLOR = "#E0E0E0"  # Светло-серый
    ACCENT_COLOR = "#FF7B30"  # Ржавый оранжевый
    BUTTON_BG = "#2D2D2D"
    BUTTON_ACTIVE = "#8B0000"

    TITLE_STYLE = {"font": ("Courier New", 24, "bold"), "bg": BG_COLOR, "fg": ACCENT_COLOR}
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

    # Текст правил игры
    RULES_TEXT = """

    Перед тем как начать игру, решите как вы создадите сеть. Это может быть вертуальная сеть, или локальная
    Тот кто вписывает IP сервера, должен передать его другим игрокам, для того, чтобы оказаться в одной сети

    НАЧАЛО АПОКАЛИПСИСА

    Начался апокалипсис, и вы собрались у бункера, но в него может попасть только половина из вас из-за ограниченного места.

    ХАРАКТЕРИСТИКИ ИГРОКОВ:

    У каждого персонажа есть уникальные карты:
    Профессия, здоровье, хобби и т.д. Все они характеризуют вашего персонажа, с ними вы должны убедить других впустить вас
    Также у вас есть карта условия - это карта со специальным действием, которую вы можете сырать в любой момент игры, если только
    вас не выгнали

    ХОД ИГРЫ:

    1. НАЧАЛО ИГРЫ - Нажмите на значок ☣ биологической опасности слева, чтобы узнать:
    - Тип апокалипсиса
    - Доступные в бункере ресурсы и помещения
    - Условия выживания

    2. ИГРОВОЙ ПРОЦЕСС - Каждый раунд:
    • Открывайте карты согласно указаниям в кнопке "?". Вы должны назвать текст карты, сказать чем она полезна, или же
      попытаться из плохой превратить в хорошую или нейтральную
    • Следите за номером раунда - с определённого момента начинается голосование за исключение игроков

    3. ЗАВЕРШЕНИЕ ИГРЫ - Когда останется ровно половина игроков:
    • Нажмите на символ ☣ биологической опасности
    • Узнайте концовку и угрозы для вашего бункер
    • Получите рекомендации по выживанию

    ЦЕЛЬ ИГРЫ: Оставить в бункере самых ценных для выживания персонажей, используя убеждение и стратегическое мышление.

    Удачи! Пусть победит тот, кто умеет убеждать. Да начнется игра!
    """

    def back_window():
        okno.destroy()
        import podmain
        podmain.podmaini(icon_png, icon_ico, db_path)

    # Создание основного окна
    okno = tk.Tk()
    okno.configure(bg=BG_COLOR)
    okno.title("Бункер")
    if sys.platform.startswith('win'):
        okno.state('zoomed')
    else:
        try:
            okno.attributes('-zoomed', True)
        except:
            okno.state('normal')

    if sys.platform.startswith('win'):
        if icon_ico and os.path.exists(icon_ico):
            okno.iconbitmap(icon_ico)
    else:
        try:
            if icon_png and os.path.exists(icon_png):
                okno.iconphoto(icon_png)
        except: pass

    # Настройка сетки
    okno.columnconfigure(0, weight=1)

    # Заголовок
    title = tk.Label(okno, text="Правила игры", **TITLE_STYLE)
    title.grid(column=0, row=0, pady=20)

    # Кнопка назад
    back = tk.Button(okno, text="←", command=back_window, **BACK_BUTTON_STYLE)
    back.place(x=20, y=20)

    # Текст правил с прокруткой
    frame = tk.Frame(okno, bg=BG_COLOR)
    frame.grid(column=0, row=1, sticky="nsew", padx=50, pady=10)
    okno.rowconfigure(1, weight=1)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    rules_text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set,
                        font=("Arial", 14), 
                        bg=BG_COLOR, 
                        fg=TEXT_COLOR,
                        padx=20, 
                        pady=20,
                        relief="flat",
                        borderwidth=0,
                        spacing2=5)
    rules_text.pack(side="left", fill="both", expand=True)
    rules_text.insert("1.0", RULES_TEXT)
    rules_text.config(state="disabled")

    scrollbar.config(command=rules_text.yview)

    okno.mainloop()

# Для тестирования
if __name__ == "__main__":
    rules("icon.ico", "database.db")