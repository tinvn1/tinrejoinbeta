import os
import time
import requests
import json
import sys
import select
import tty
import termios

CONFIG_FILE = "config_rejoin.json"
FALLBACK_CONFIG_FILE = "/sdcard/Download/config_rejoin.json"

LANG = {
    "VNI": {
        "status_title": "STATUS SYSTEM",
        "status_map": {
            0: "OFFLINE 🔴",
            1: "ONLINE (Chỉ lướt Web) 🌐",
            2: "IN-GAME (Đang chơi game) 🎮",
            3: "IN STUDIO 🛠️"
        },
        "menu_title": "[ MENU CẤU HÌNH TỰ ĐỘNG ]",
        "m1": "[1] Khởi động Tool Rejoin",
        "m2": "[2] Cài đặt Server & Account (User ID, Place ID, VIP)",
        "m3": "[3] Cài đặt Thời Gian (Check Interval & Force Rejoin)",
        "m4": "[4] Ngôn ngữ / Language",
        "m5": "[5] Xóa cấu hình hiện tại",
        "m0": "[0] Thoát hệ thống",
        "choice": "👉 CHẠM TRỰC TIẾP VÀO DÒNG MENU ĐỂ CHỌN",
        "running": "TOOL ĐANG HOẠT ĐỘNG NGẦM...",
        "btn_pause": " [ ⏸️ CHẠM VÀO ĐÂY ĐỂ TẠM DỪNG / TIẾP TỤC ] ",
        "btn_stop":  " [ 🛑 CHẠM VÀO ĐÂY ĐỂ DỪNG HẲN / THOÁT TOOL ] ",
        "paused_msg": "⏸️ [ĐÃ TẠM DỪNG] Chạm nút PAUSE để chạy tiếp | STOP để thoát...",
        "force_rejoin": "ĐÃ ĐẾN HẸN ÉP REJOIN ĐỊNH KỲ!",
        "offline_warn": "Phát hiện acc văng trận/offline!"
    },
    "ENG": {
        "status_title": "SYSTEM STATUS",
        "status_map": {
            0: "OFFLINE 🔴",
            1: "ONLINE (Web Browsing) 🌐",
            2: "IN-GAME (Playing Game) 🎮",
            3: "IN STUDIO 🛠️"
        },
        "menu_title": "[ AUTOMATION MENU CONFIG ]",
        "m1": "[1] Start Rejoin Tool",
        "m2": "[2] Setup Server & Account (User ID, Place ID, VIP)",
        "m3": "[3] Setup Timer Options (Check & Force Rejoin Interval)",
        "m4": "[4] Language Settings",
        "m5": "[5] Delete Current Config",
        "m0": "[0] Exit System",
        "choice": "👉 TAP DIRECTLY ON ANY MENU LINE TO CHOOSE",
        "running": "TOOL IS RUNNING IN BACKGROUND...",
        "btn_pause": " [ ⏸️ TAP HERE TO PAUSE / RESUME ] ",
        "btn_stop":  " [ 🛑 TAP HERE TO STOP FULLY / EXIT ] ",
        "paused_msg": "⏸️ [PAUSED] Tap PAUSE button to resume | STOP to exit...",
        "force_rejoin": "SCHEDULED FORCE REJOIN TRIGGERED!",
        "offline_warn": "Account disconnected / offline detected!"
    }
}

current_lang = "VNI"

def enable_mouse():
    sys.stdout.write("\033[?1000h\033[?1006h")
    sys.stdout.flush()

def disable_mouse():
    sys.stdout.write("\033[?1000l\033[?1006l")
    sys.stdout.flush()

def get_active_config_path():
    if os.path.exists(CONFIG_FILE):
        return CONFIG_FILE
    elif os.path.exists(FALLBACK_CONFIG_FILE):
        return FALLBACK_CONFIG_FILE
    return CONFIG_FILE

def load_config():
    path = get_active_config_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config_data):
    path = get_active_config_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
    except Exception:
        with open(FALLBACK_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)

def Banner():
    os.system("clear")
    print("\033[1;36m")
    print(" ████████╗██╗███╗   ██╗██╗  ██╗██╗   ██╗██████╗ ")
    print(" ╚══██╔══╝██║████╗  ██║██║  ██║██║   ██║██╔══██╗")
    print("    ██║   ██║██╔██╗ ██║███████║██║   ██║██████╔╝")
    print("    ██║   ██║██║╚██╗██║██╔══██║██║   ██║██╔══██╗")
    print("    ██║   ██║██║ ╚████║██║  ██║╚██████╔╝██████╔╝")
    print("    ╚═╝   ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ")
    print("\033[1;32m=======================================================\033[0m")
    print("\033[1;37m        🚀 TINHUB REJOIN SYSTEM AUTOMATION v4.2 🚀\033[0m")
    print("\033[1;32m=======================================================\033[0m\n")

def read_input_event():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        buf = sys.stdin.read(1)
        if buf == '\033':
            time.sleep(0.01)
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                buf += sys.stdin.read(1)
            if buf.startswith("\033[<") and ('m' in buf or 'M' in buf):
                try:
                    parts = buf[3:-1].split(';')
                    if len(parts) >= 3 and parts[0] in ['0', '2']:
                        x = int(parts[1])
                        y = int(parts[2])
                        return ("TOUCH", x, y)
                except:
                    pass
        return ("KEY", buf)
    return None

def print_status_box(user_id, status_text, next_rejoin_s, is_paused=False):
    l = LANG[current_lang]
    state_display = "PAUSED ⏸️" if is_paused else status_text
    print("\033[1;34m┌─────────────────────────────────────────────────────┐\033[0m")
    print(f"\033[1;34m│\033[0m  \033[1;33m📌 {l['status_title']}\033[0m                                 \033[1;34m│\033[0m")
    print(f"\033[1;34m│\033[0m  👤 User ID : \033[1;36m{user_id:<36}\033[0m \033[1;34m│\033[0m")
    print(f"\033[1;34m│\033[0m  📊 State   : \033[1;32m{state_display:<36}\033[0m \033[1;34m│\033[0m")
    print(f"\033[1;34m│\033[0m  ⏳ Rejoin In: \033[1;35m{str(next_rejoin_s) + 's':<35}\033[0m \033[1;34m│\033[0m")
    print("\033[1;34m└─────────────────────────────────────────────────────┘\033[0m")

# 1. SETUP CẤU HÌNH SERVER & ACCOUNT (TÁCH RIÊNG)
def setup_server_config():
    disable_mouse()
    Banner()
    print("\033[1;33m[🌐] SETUP SERVER & ACCOUNT / CÀI ĐẶT SERVER & ACC\033[0m\n")
    try:
        user_id = int(input("\033[1;32m[1] Roblox User ID:\033[0m ").strip())
        place_id = input("\033[1;32m[2] Game Place ID:\033[0m ").strip()
        vip_link = input("\033[1;32m[3] VIP Server Link (Nhấn ENTER để bỏ qua):\033[0m ").strip()
    except ValueError:
        print("\n\033[1;31m[❌] Input Error / Lỗi nhập liệu!\033[0m")
        time.sleep(2)
        enable_mouse()
        return None

    config = load_config()
    config.update({
        "user_id": user_id,
        "place_id": place_id,
        "vip_link": vip_link,
        "lang": current_lang
    })
    save_config(config)
    print("\n\033[1;32m[💾] Đã lưu thông tin Server & Account thành công!\033[0m")
    time.sleep(1.5)
    enable_mouse()
    return config

# 2. SETUP THỜI GIAN CHECK (TÁCH RIÊNG)
def setup_timer_config():
    disable_mouse()
    Banner()
    print("\033[1;33m[⏱️] SETUP TIMER / CÀI ĐẶT THỜI GIAN CHECK & REJOIN\033[0m\n")
    try:
        check_interval = int(input("\033[1;32m[1] Thời gian kiểm tra status (Giây, Mặc định 15s):\033[0m ").strip() or "15")
        force_interval = int(input("\033[1;32m[2] Thời gian ép Rejoin định kỳ (Phút, Mặc định 60p):\033[0m ").strip() or "60")
    except ValueError:
        print("\n\033[1;31m[❌] Input Error / Lỗi nhập liệu!\033[0m")
        time.sleep(2)
        enable_mouse()
        return None

    config = load_config()
    config.update({
        "check_interval": check_interval,
        "force_interval": force_interval
    })
    save_config(config)
    print("\n\033[1;32m[💾] Đã lưu thiết lập thời gian thành công!\033[0m")
    time.sleep(1.5)
    enable_mouse()
    return config

def check_roblox_presence(user_id):
    url = "https://presence.roblox.com/v1/presence/users"
    headers = {"Content-Type": "application/json"}
    payload = {"userIds": [user_id]}
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data and "userPresences" in data and len(data["userPresences"]) > 0:
                return data["userPresences"][0].get("userPresenceType", 0)
    except Exception:
        pass
    return 0 

def kill_and_launch_roblox(place_id, vip_url):
    print("\n\033[1;31m[💥] KILLING ROBLOX APP...\033[0m")
    os.system("su -c 'am force-stop com.roblox.client' 2>/dev/null || am force-stop com.roblox.client")
    time.sleep(2)
    intent_url = vip_url if (vip_url and vip_url.startswith("http")) else f"roblox://placeId={place_id}"
    os.system(f"su -c \"am start -a android.intent.action.VIEW -d '{intent_url}' com.roblox.client\" 2>/dev/null || am start -a android.intent.action.VIEW -d '{intent_url}'")

def run_tool(config):
    global current_lang
    l = LANG[current_lang]
    USER_ID = config.get("user_id")
    PLACE_ID = config.get("place_id")
    VIP_LINK = config.get("vip_link", "")
    
    if not USER_ID or not PLACE_ID:
        print("\n\033[1;31m[⚠️] Chưa cài đặt Server & User ID! Vui lòng chọn mục [2] để cài đặt trước.\033[0m")
        time.sleep(2.5)
        return

    check_interval = config.get("check_interval", 15)
    force_interval = config.get("force_interval", 60)

    force_timeout = force_interval * 60
    start_time = time.time()
    is_paused = False

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        enable_mouse()
        
        while True:
            Banner()
            print(f"\033[1;35m[▶️] {l['running']}\033[0m\n")

            elapsed_time = time.time() - start_time
            time_left = max(0, int(force_timeout - elapsed_time))

            print(f"\033[1;44;37m{l['btn_pause']}\033[0m\n")
            print(f"\033[1;41;37m{l['btn_stop']}\033[0m\n")

            if is_paused:
                print_status_box(USER_ID, "PAUSED ⏸️", time_left, is_paused=True)
                print(f"\n\033[1;33m{l['paused_msg']}\033[0m")
                
                while is_paused:
                    evt = read_input_event()
                    if evt:
                        kind = evt[0]
                        if kind == "TOUCH":
                            y = evt[2]
                            if 16 <= y <= 18:
                                is_paused = False
                                break
                            elif 18 < y <= 20:
                                print("\n\033[1;31m[🛑] STOPPED BY TOUCH!\033[0m")
                                time.sleep(1.5)
                                return
                        elif kind == "KEY":
                            if evt[1] == ' ':
                                is_paused = False
                                break
                            elif evt[1] in ['s', 'S']:
                                return
                    time.sleep(0.2)
                continue

            if elapsed_time >= force_timeout:
                print(f"\n\033[1;33m[🔥] {l['force_rejoin']}\033[0m")
                kill_and_launch_roblox(PLACE_ID, VIP_LINK)
                start_time = time.time()
                time.sleep(45)
                continue

            status = check_roblox_presence(USER_ID)
            status_text = l["status_map"].get(status, "UNKNOWN")
            
            print_status_box(USER_ID, status_text, time_left)

            if status != 2:
                print(f"\n\033[1;31m[⚠️] {l['offline_warn']}\033[0m")
                kill_and_launch_roblox(PLACE_ID, VIP_LINK)
                time.sleep(45)
            else:
                for _ in range(check_interval * 5):
                    evt = read_input_event()
                    if evt:
                        kind = evt[0]
                        if kind == "TOUCH":
                            y = evt[2]
                            if 16 <= y <= 18:
                                is_paused = True
                                break
                            elif 18 < y <= 20:
                                print("\n\033[1;31m[🛑] STOPPED BY TOUCH!\033[0m")
                                time.sleep(1.5)
                                return
                        elif kind == "KEY":
                            if evt[1] == ' ':
                                is_paused = True
                                break
                            elif evt[1] in ['s', 'S']:
                                return
                    time.sleep(0.2)

    except KeyboardInterrupt:
        pass
    finally:
        disable_mouse()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def change_language():
    global current_lang
    Banner()
    print("\033[1;36m[ LANGUAGE SETTINGS / CÀI ĐẶT NGÔN NGỮ ]\033[0m\n")
    print(" 👉 [Chạm dòng này]: Tiếng Việt (VNI)")
    print(" 👉 [Chạm dòng này]: English (ENG)\n")
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        enable_mouse()
        while True:
            evt = read_input_event()
            if evt:
                if evt[0] == "TOUCH":
                    y = evt[2]
                    if y == 13:
                        current_lang = "VNI"
                        break
                    elif y == 14:
                        current_lang = "ENG"
                        break
                elif evt[0] == "KEY":
                    if evt[1] == '1':
                        current_lang = "VNI"
                        break
                    elif evt[1] == '2':
                        current_lang = "ENG"
                        break
            time.sleep(0.1)
    finally:
        disable_mouse()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    cfg = load_config()
    cfg["lang"] = current_lang
    save_config(cfg)

def main():
    global current_lang
    cfg = load_config()
    if "lang" in cfg:
        current_lang = cfg["lang"]

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    while True:
        Banner()
        l = LANG[current_lang]
        print(f"\033[1;32m{l['menu_title']}\033[0m")
        print(f" \033[1;36m{l['m1']}\033[0m") # Dòng Y = 13
        print(f" \033[1;36m{l['m2']}\033[0m") # Dòng Y = 14
        print(f" \033[1;36m{l['m3']}\033[0m") # Dòng Y = 15
        print(f" \033[1;36m{l['m4']}\033[0m") # Dòng Y = 16
        print(f" \033[1;36m{l['m5']}\033[0m") # Dòng Y = 17
        print(f" \033[1;31m{l['m0']}\033[0m") # Dòng Y = 18
        print("=======================================================")
        print(f"\033[1;33m{l['choice']}\033[0m\n")

        try:
            tty.setcbreak(fd)
            enable_mouse()
            
            choice = None
            while not choice:
                evt = read_input_event()
                if evt:
                    if evt[0] == "TOUCH":
                        y = evt[2]
                        if y == 13: choice = "1"
                        elif y == 14: choice = "2"
                        elif y == 15: choice = "3"
                        elif y == 16: choice = "4"
                        elif y == 17: choice = "5"
                        elif y == 18: choice = "0"
                    elif evt[0] == "KEY":
                        choice = evt[1]
                time.sleep(0.05)

        finally:
            disable_mouse()
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if choice == "1":
            config = load_config()
            if config and "user_id" in config:
                run_tool(config)
            else:
                config = setup_server_config()
                if config:
                    run_tool(config)
        elif choice == "2":
            setup_server_config()
        elif choice == "3":
            setup_timer_config()
        elif choice == "4":
            change_language()
        elif choice == "5":
            path = get_active_config_path()
            if os.path.exists(path):
                os.remove(path)
                print("\n\033[1;32m[🗑️] Config Deleted / Đã xóa cấu hình!\033[0m")
            time.sleep(1.5)
        elif choice == "0":
            sys.exit()

if __name__ == "__main__":
    main()
