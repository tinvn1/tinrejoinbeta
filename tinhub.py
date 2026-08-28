import os
import time
import requests
import json
import sys
import re

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
        "m2": "[2] Cài đặt Server & Account (Auto/Manual)",
        "m3": "[3] Cài đặt Thời Gian (Check Interval & Force Rejoin)",
        "m4": "[4] Ngôn ngữ / Language",
        "m5": "[5] Xóa cấu hình hiện tại",
        "m0": "[0] Thoát hệ thống",
        "choice": "👉 Nhập lựa chọn của bạn: ",
        "running": "TOOL ĐANG HOẠT ĐỘNG NGẦM...",
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
        "m2": "[2] Setup Server & Account (Auto/Manual)",
        "m3": "[3] Setup Timer Options (Check & Force Rejoin Interval)",
        "m4": "[4] Language Settings",
        "m5": "[5] Delete Current Config",
        "m0": "[0] Exit System",
        "choice": "👉 Enter your choice: ",
        "running": "TOOL IS RUNNING IN BACKGROUND...",
        "force_rejoin": "SCHEDULED FORCE REJOIN TRIGGERED!",
        "offline_warn": "Account disconnected / offline detected!"
    }
}

current_lang = "VNI"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

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
        except Exception:
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
    print(" ████████╗██╗███╗    ██╗██╗   ██╗██╗   ██╗██████╗ ")
    print(" ╚══██╔══╝██║████╗   ██║██║   ██║██║   ██║██╔══██╗")
    print("    ██║   ██║██╔██╗ ██║███████║██║   ██║██████╔╝")
    print("    ██║   ██║██║╚██╗██║██╔══██║██║   ██║██╔══██╗")
    print("    ██║   ██║██║ ╚████║██║   ██║╚██████╔╝██████╔╝")
    print("    ╚═╝   ╚═╝╚═╝  ╚═══╝╚═╝   ╚═══╝ ╚═════╝ ╚═════╝ ")
    print("\033[1;32m=======================================================\033[0m")
    print("\033[1;37m        🚀 TINHUB REJOIN SYSTEM AUTOMATION v4.4 🚀\033[0m")
    print("\033[1;32m=======================================================\033[0m\n")

def print_status_box(user_id, status_text, next_rejoin_s, check_in, force_in):
    l = LANG[current_lang]
    print("\033[1;34m┌─────────────────────────────────────────────────────┐\033[0m")
    print(f"\033[1;34m│\033[0m  \033[1;33m📌 {l['status_title']}\033[0m                                 \033[1;34m│\033[0m")
    print(f"\033[1;34m│\033[0m  👤 User ID   : \033[1;36m{str(user_id):<34}\033[0m \033[1;34m│\033[0m")
    print(f"\033[1;34m│\033[0m  📊 State     : \033[1;32m{status_text:<34}\033[0m \033[1;34m│\033[0m")
    print(f"\033[1;34m│\033[0m  ⏱️ Config    : \033[1;33mCheck {check_in}s | Force {force_in}p\033[0m          \033[1;34m│\033[0m")
    print(f"\033[1;34m│\033[0m  ⏳ Rejoin In : \033[1;35m{str(next_rejoin_s) + 's':<34}\033[0m \033[1;34m│\033[0m")
    print("\033[1;34m└─────────────────────────────────────────────────────┘\033[0m")

def get_user_id_from_username(username):
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username], "excludeBannedUsers": False}
    try:
        res = requests.post(url, json=payload, headers=HEADERS, timeout=8)
        if res.status_code == 200:
            data = res.json().get("data", [])
            if data and len(data) > 0:
                user_info = data[0]
                return user_info.get("id"), user_info.get("displayName")
    except Exception:
        pass
    return None, None

def extract_place_id_from_vip(vip_link):
    match = re.search(r'/games/(\d+)', vip_link)
    if match:
        return match.group(1)
    return None

def search_game_by_name(game_keyword):
    """
    Tìm kiếm game theo từ khóa và trả về Place ID của kết quả chọn.
    """
    url = f"https://games.roblox.com/v1/games/list?model.keyword={requests.utils.quote(game_keyword)}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            games = res.json().get("games", [])
            if not games:
                print("\033[1;31m[❌] Không tìm thấy game nào khớp với từ khóa!\033[0m")
                return None
            
            print("\n\033[1;36m[🔎] KẾT QUẢ TÌM KIẾM GAME:\033[0m")
            top_games = games[:5]  # Lấy tối đa 5 kết quả đầu
            for idx, g in enumerate(top_games, 1):
                name = g.get("name", "Unknown")
                place_id = g.get("placeId", "N/A")
                builder = g.get("builder", "Unknown")
                print(f" \033[1;33m[{idx}]\033[0m \033[1;37m{name}\033[0m | Place ID: \033[1;32m{place_id}\033[0m (Tác giả: {builder})")
            
            print(" \033[1;31m[0] Bỏ qua / Nhập bằng phương thức khác\033[0m")
            sel = input("\n👉 Chọn số tương ứng với Game của bạn: ").strip()
            
            if sel.isdigit() and 1 <= int(sel) <= len(top_games):
                selected_place_id = str(top_games[int(sel) - 1].get("placeId"))
                print(f"\033[1;32m[✔] Đã lựa chọn Game ID: {selected_place_id}\033[0m")
                return selected_place_id
    except Exception as e:
        print(f"\033[1;31m[❌] Lỗi khi tra cứu Roblox Game API: {e}\033[0m")
    return None

def setup_server_config():
    Banner()
    print("\033[1;33m[🌐] SETUP SERVER & ACCOUNT (TỰ ĐỘNG / THỦ CÔNG)\033[0m\n")
    
    # 1. Nhập User Info
    user_input = input("\033[1;32m[1] Nhập Username HOẶC Roblox User ID:\033[0m ").strip()
    user_id = None
    
    if user_input.isdigit():
        user_id = int(user_input)
        print(f"\033[1;32m[✔] Đã nhận Roblox User ID: {user_id}\033[0m")
    else:
        print("\033[1;33m[🔍] Đang tìm User ID từ Roblox API...\033[0m")
        user_id, display_name = get_user_id_from_username(user_input)
        if user_id:
            print(f"\033[1;32m[✔] Đã tìm thấy Acc: {display_name} (@{user_input})\033[0m")
            print(f"\033[1;32m[✔] User ID: {user_id}\033[0m")
        else:
            print("\033[1;31m[❌] Không tìm thấy Username này trên Roblox! Kiểm tra lại chính tả.\033[0m")
            time.sleep(2.5)
            return None

    # 2. Xử lý Link VIP nếu có
    vip_link = input("\n\033[1;32m[2] Dán Link Server VIP (Ấn ENTER nếu không dùng VIP):\033[0m ").strip()
    place_id = None

    if vip_link and vip_link.startswith("http"):
        place_id = extract_place_id_from_vip(vip_link)
        if place_id:
            print(f"\033[1;32m[✔] Đã tự động tách Game Place ID từ Link VIP: {place_id}\033[0m")

    # 3. Tìm kiếm Game Name hoặc Nhập Place ID Thủ Công (nếu chưa có từ Link VIP)
    if not place_id:
        print("\n\033[1;36m[3] CẤU HÌNH GAME PLACE ID:\033[0m")
        print(" \033[1;33m[A]\033[0m Tìm kiếm theo Tên Game")
        print(" \033[1;33m[B]\033[0m Nhập Place ID trực tiếp")
        method = input("👉 Lựa chọn phương thức (A/B, mặc định A): ").strip().upper() or "A"
        
        if method == "A":
            game_kw = input("\n👉 Nhập tên Game muốn tìm (VD: Art to Destroy, Blox Fruits...): ").strip()
            if game_kw:
                place_id = search_game_by_name(game_kw)
        
        # Nếu phương thức B hoặc tìm kiếm A không chọn được ID
        if not place_id:
            place_id = input("\n\033[1;32m👉 Nhập Game Place ID thủ công:\033[0m ").strip()
            
        if not place_id:
            print("\n\033[1;31m[❌] Place ID không được để trống!\033[0m")
            time.sleep(2)
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
    return config

def setup_timer_config():
    Banner()
    print("\033[1;33m[⏱️] SETUP TIMER / CÀI ĐẶT THỜI GIAN CHECK & REJOIN\033[0m\n")
    try:
        check_interval = int(input("\033[1;32m[1] Thời gian kiểm tra status (Giây, Mặc định 15s):\033[0m ").strip() or "15")
        force_interval = int(input("\033[1;32m[2] Thời gian ép Rejoin định kỳ (Phút, Mặc định 60p):\033[0m ").strip() or "60")
    except ValueError:
        print("\n\033[1;31m[❌] Input Error / Lỗi nhập liệu!\033[0m")
        time.sleep(2)
        return None

    config = load_config()
    config.update({
        "check_interval": check_interval,
        "force_interval": force_interval
    })
    save_config(config)
    print("\n\033[1;32m[💾] Đã lưu thiết lập thời gian thành công!\033[0m")
    time.sleep(1.5)
    return config

def check_roblox_presence(user_id):
    url = "https://presence.roblox.com/v1/presence/users"
    payload = {"userIds": [user_id]}
    try:
        res = requests.post(url, json=payload, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data and "userPresences" in data and len(data["userPresences"]) > 0:
                return data["userPresences"][0].get("userPresenceType", 0)
    except Exception:
        pass
    return 0 

def kill_and_launch_roblox(place_id, vip_url):
    print("\n\033[1;31m[💥] KILLING ROBLOX APP...\033[0m")
    pkg = "com.roblox.client"
    
    os.system(f"su -c 'am force-stop {pkg} >/dev/null 2>&1'")
    os.system(f"su -c 'pkill -f {pkg} >/dev/null 2>&1'")
    os.system(f"am force-stop {pkg} >/dev/null 2>&1")
    
    time.sleep(2)
    
    intent_url = vip_url if (vip_url and vip_url.startswith("http")) else f"roblox://placeId={place_id}"
    
    print("\033[1;32m[🚀] RE-LAUNCHING ROBLOX...\033[0m")
    os.system(f"su -c 'am start -a android.intent.action.VIEW -d \"{intent_url}\" {pkg} >/dev/null 2>&1'")
    os.system(f"am start -a android.intent.action.VIEW -d \"{intent_url}\" {pkg} >/dev/null 2>&1")

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

    try:
        check_interval = int(config.get("check_interval", 15))
    except (ValueError, TypeError):
        check_interval = 15

    try:
        force_interval = int(config.get("force_interval", 60))
    except (ValueError, TypeError):
        force_interval = 60

    force_timeout = force_interval * 60
    start_time = time.time()

    print("\n\033[1;33m[💡] Nhấn Ctrl + C bất kỳ lúc nào để dừng Tool và quay lại Menu.\033[0m")
    time.sleep(2)

    try:
        while True:
            Banner()
            print(f"\033[1;35m[▶️] {l['running']}\033[0m\n")

            elapsed_time = time.time() - start_time
            time_left = max(0, int(force_timeout - elapsed_time))

            if elapsed_time >= force_timeout:
                print(f"\n\033[1;33m[🔥] {l['force_rejoin']}\033[0m")
                kill_and_launch_roblox(PLACE_ID, VIP_LINK)
                start_time = time.time()
                print("\033[1;36m[⏳] Đang chờ game tải vào lại (30s)...\033[0m")
                time.sleep(30)
                continue

            status = check_roblox_presence(USER_ID)
            status_text = l["status_map"].get(status, "UNKNOWN")
            
            print_status_box(USER_ID, status_text, time_left, check_interval, force_interval)

            if status != 2:
                print(f"\n\033[1;31m[⚠️] {l['offline_warn']}\033[0m")
                kill_and_launch_roblox(PLACE_ID, VIP_LINK)
                print("\033[1;36m[⏳] Đang chờ game tải vào lại (30s)...\033[0m")
                time.sleep(30)
            else:
                time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\n\033[1;31m[🛑] Đã dừng Tool Rejoin. Đang quay lại Menu...\033[0m")
        time.sleep(1.5)

def change_language():
    global current_lang
    Banner()
    print("\033[1;36m[ LANGUAGE SETTINGS / CÀI ĐẶT NGÔN NGỮ ]\033[0m\n")
    print(" \033[1;36m[1] Tiếng Việt (VNI)\033[0m")
    print(" \033[1;36m[2] English (ENG)\033[0m")
    print(" \033[1;31m[0] Quay lại / Back\033[0m\n")
    
    choice = input("👉 Chọn ngôn ngữ / Choose language: ").strip()
    if choice == "1":
        current_lang = "VNI"
    elif choice == "2":
        current_lang = "ENG"
    else:
        return

    cfg = load_config()
    cfg["lang"] = current_lang
    save_config(cfg)
    print(f"\n\033[1;32m[✔] Language changed to {current_lang}!\033[0m")
    time.sleep(1)

def main():
    global current_lang
    cfg = load_config()
    if "lang" in cfg and cfg["lang"] in LANG:
        current_lang = cfg["lang"]

    while True:
        Banner()
        l = LANG[current_lang]
        print(f"\033[1;32m{l['menu_title']}\033[0m")
        print(f" \033[1;36m{l['m1']}\033[0m")
        print(f" \033[1;36m{l['m2']}\033[0m")
        print(f" \033[1;36m{l['m3']}\033[0m")
        print(f" \033[1;36m{l['m4']}\033[0m")
        print(f" \033[1;36m{l['m5']}\033[0m")
        print(f" \033[1;31m{l['m0']}\033[0m")
        print("=======================================================")
        
        choice = input(f"\033[1;33m{l['choice']}\033[0m").strip()

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
