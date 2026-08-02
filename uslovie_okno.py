import tkinter as tk
import os
import sys
import requests

# Словарь действий - мост между старой БД и новой архитектурой
ACTION_MAPPING = {
    "Поменяйся профессией": {"action": "SWAP_TRAIT", "target": "PLAYER", "trait": "Профессия"},
    "Поменяйся здоровьем": {"action": "SWAP_TRAIT", "target": "PLAYER", "trait": "Здоровье"},
    "Поменяйся хобби": {"action": "SWAP_TRAIT", "target": "PLAYER", "trait": "Хобби"},
    "Поменяйся фобией": {"action": "SWAP_TRAIT", "target": "PLAYER", "trait": "Фобия"},
    "Поменяйся характером": {"action": "SWAP_TRAIT", "target": "PLAYER", "trait": "Характер"},
    "Поменяйся фактами": {"action": "SWAP_TRAIT", "target": "PLAYER", "trait": "Факты"},
    "Поменяйся багажом": {"action": "SWAP_TRAIT", "target": "PLAYER", "trait": "Багаж"},
    "Поменяйся любой характеристикой": {"action": "SWAP_TRAIT", "target": "PLAYER_AND_TRAIT"},

    "Твой возраст теперь равен возрасту любого выбранного игрока": {"action": "CHANGE_AGE", "target": "PLAYER"},
    "Выбранный игрок становится беременным": {"action": "MAKE_PREGNANT", "target": "PLAYER"},
    "Измени пол себе или другому игроку": {"action": "CHANGE_GENDER", "target": "PLAYER", "allow_self": True},

    "Запрети использовать карту условия": {"action": "BAN_VOTE", "target": "PLAYER"},

    "Выбери тип карты, который должны открыть все до конца раунда": {"action": "REVEAL_ALL", "target": "TRAIT"},
    "Раскрой любую неоткрытую характеристику игрока": {"action": "REVEAL_ANY", "target": "PLAYER_AND_TRAIT"},
    
    "Сыграй последнюю карту условий": {"action": "PLAY_LAST", "target": "NONE"}
}

def get_payload(text):
    if not text: return None
    for key, payload in ACTION_MAPPING.items():
        if key in text:
            return payload
    return None

def usl_okno(player, icon_png, icon_ico, players, code, ip, text):
    payload = get_payload(text)
    
    # Если карточка не интерактивная или не найдена в словаре - игнорируем
    if not payload:
        print(f"Неинтерактивное условие (для голосования) или неизвестно: {text}")
        return

    # Цвета и стили
    BG_COLOR = "#1A1A1A"
    TEXT_COLOR = "#E0E0E0"
    ACCENT_COLOR = "#FF7B30"
    BUTTON_BG = "#2D2D2D"
    BUTTON_ACTIVE = "#CC5500"

    HEADING_STYLE = {"font": ("Arial", 16, "bold"), "bg": BG_COLOR, "fg": ACCENT_COLOR}
    BUTTON_STYLE = {"font": ("Arial", 12), "bg": BG_COLOR, "fg": TEXT_COLOR, 'height':3}
    PADDING = {"pady": 5, 'padx':(10,0)}

    okno = tk.Toplevel()
    okno.configure(background=BG_COLOR)
    okno.geometry('535x450')
    okno.title("Окно условия")

    if sys.platform.startswith('win') and icon_ico and os.path.exists(icon_ico):
        okno.iconbitmap(icon_ico)
    elif icon_png and os.path.exists(icon_png):
        try:
            img = tk.PhotoImage(file=icon_png)
            okno.iconphoto(True, img)
        except:
            pass

    # Универсальная функция отправки Payload на сервер
    def execute_action(target_player=None, selected_trait=None, char_index=None):
        data = {
            "player": f"igrok{player}",
            "players": players,
            "target_player": f"igrok{target_player}" if target_player else None,
            "selected_trait": selected_trait,
            "char_index": char_index,
            "card_data": payload,
            "text": text
        }
        
        if payload["action"] == "PLAY_LAST":
            last_text = requests.get(f'http://{ip}/rooms/{code}/uslovie/last').json()
            okno.destroy()
            usl_okno(player, icon_png, icon_ico, players, code, ip, last_text)
            return

        requests.post(f'http://{ip}/rooms/{code}/execute_action', json=data)
        okno.destroy()

    def clear_and_show_traits(target_p=None):
        for widget in okno.winfo_children():
            widget.destroy()
        make_chars(target_p)

    def make_net():
        mesto = [[],[],[]]
        for i in range(1, len(players) + 1):
            if i <= 4: mesto[0].append(i)
            elif i <= 8: mesto[1].append(i)
            else: mesto[2].append(i)

        if not payload.get("allow_self", False):
            for group in mesto:
                if player in group: group.remove(player)

        for i in range(9): okno.grid_columnconfigure(i, weight=1)
        title = tk.Label(okno, text="Выберите игрока", **HEADING_STYLE)
        title.grid(column=0, row=0, columnspan=9, sticky='ew')

        templates = {
            1: ['', '', '', 'k', '', '', ''],
            2: ['', '', 'k', '', 'k', '', ''],
            3: ['', 'k', '', 'k', '', 'k', ''],
            4: ['k', '', 'k', '', 'k', '', 'k']
        }

        row = 1
        for group in mesto:
            if not group: continue
            template = templates[len(group)]
            col = 1
            for t in template:
                if t == 'k':
                    player_num = group.pop(0)
                    
                    if payload["target"] == "PLAYER_AND_TRAIT":
                        comanda = lambda p=player_num: clear_and_show_traits(p)
                    else:
                        comanda = lambda p=player_num: execute_action(target_player=p)
                        
                    btn = tk.Button(okno, text=player_num, **BUTTON_STYLE, command=comanda, width=3)
                    btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
                col += 1
            row += 1

    def make_chars(target_p=None):
        title = tk.Label(okno,text="Выберите тип карты", **HEADING_STYLE)
        title.grid(column=1, row=0,columnspan=2, sticky='ew')
        chars = [
            ["🔧 Профессия",'Профессия',0], ["🧬 Биология",'Биология',1],
            ['🤧 Здоровье',"Здоровье",2], ["🎯 Хобби","Хобби",3],
            ["😨 Фобия","Фобия",4], ["🧠 Характер","Характер",5],
            ["📝 Факт","Факт",6], ["🎒 Багаж","Багаж",7]
        ]
        row = 1
        column = 0
        for label, char_name, char_index in chars:
            btn = tk.Button(okno,text=label, **BUTTON_STYLE,
                command=lambda cn=char_name, ci=char_index: execute_action(target_player=target_p, selected_trait=cn, char_index=ci))
            btn.grid(row=row, column=column, **PADDING)
            column += 1
            if column == 4:
                column=0
                row=2

    # Рендер в зависимости от Target
    if payload["action"] == "PLAY_LAST":
        execute_action()
    elif payload["target"] in ["PLAYER", "PLAYER_AND_TRAIT"]:
        make_net()
    elif payload["target"] == "TRAIT":
        make_chars()