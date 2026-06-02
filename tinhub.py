cat << 'EOF' > tinhub.py
import time
import os
import random
import requests
import sys
import re

# ================= CONFIG MẶC ĐỊNH =================
USER_ID = "312148668"       
GAME_TARGET = "90148635862803" 
CHECK_INTERVAL = 60         
USE_ROOT = True             
# ===================================================

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
}

def clear_screen():
    os.system('clear')

def show_banner():
    print("==================================================")
    print("      ████████╗██╗███╗   ██╗██╗  ██╗██╗   ██╗██████╗ ")
    print("      ╚══██╔══╝██║████╗  ██║██║  ██║██║   ██║██╔══██╗")
    print("         ██║   ██║██╔██╗ ██║███████║██║   ██║██████╔╝")
    print("         ██║   ██║██║╚██╗██║██╔══██║██║   ██║██╔══██╗")
    print("         ██║   ██║██║ ╚████║██║  ██║╚██████╔╝██████╔╝")
    print("         ╚═╝   ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ")
    print("           [ TinHub - ROOT & CLOUD OPTIMIZED ]      ")
    print("==================================================")

def optimize_system_root():
    if not USE_ROOT: return
    print("[+] ROOT: Đang dọn dẹp bộ nhớ đệm (Cache RAM) để giảm lag...")
    os.system("su -c 'echo 3 > /proc/sys/vm/drop_caches'")
    os.system("su -c 'echo -17 > /proc/self/oom_adj'")
    os.system("su -c 'am kill-all'")

def is_user_in_this_game(user_id):
    url_presence = "https://presence.roblox.com/v1/presence/users"
    try:
        res = requests.post(url_presence, json={"userIds": [int(user_id)]}, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()['userPresences'][0]
            return data['userPresenceType'] == 2
        return True
    except:
        print(f" [!] {time.strftime('%H:%M:%S')} | Mạng lag/Mất kết nối API. Đang bỏ qua lượt check...")
        return True

def launch_game():
    vip_mode = "roblox.com" in GAME_TARGET or "code=" in GAME_TARGET
    if vip_mode:
        match = re.search(r'code=([^&]+)', GAME_TARGET)
        vip_code = match.group(1) if match else GAME_TARGET
        deeplink = f"roblox://navigation/shareLinks?code={vip_code}&type=Server"
    else:
        deeplink = f"roblox://placeId={GAME_TARGET}"
        
    if USE_ROOT:
        print("\n[+] ROOT: Sử dụng đặc quyền su để ép mở tương thích Android 10...")
        os.system(f"su -c 'am start -a android.intent.action.VIEW -d \"{deeplink}\"'")
    else:
        print("\n[!] Không ROOT: Mở app bằng quyền thường...")
        os.system(f"am start --user 0 -a android.intent.action.VIEW -d '{deeplink}'")

def run_rejoin():
    clear_screen()
    show_banner()
    if USE_ROOT:
        optimize_system_root()
        
    mode_display = "SERVER VIP" if ("roblox.com" in GAME_TARGET or len(GAME_TARGET) > 20) else "MAP CÔNG KHAI"
    print(f" [+] Tài khoản giám sát  : {USER_ID}")
    print(f" [+] Chế độ vào game      : {mode_display}")
    print(f" [+] ROOT Tối ưu hóa      : {'ĐÃ BẬT' if USE_ROOT else 'TẮT'}")
    print(" --------------------------------------------------")
    
    while True:
        try:
            in_game = is_user_in_this_game(USER_ID)
            if not in_game:
                launch_game()
                print(f" [~] {time.strftime('%H:%M:%S')} | Đang đợi 100 giây cho máy yếu load game...")
                time.sleep(100)
                if USE_ROOT: optimize_system_root()
            else:
                random_delay = CHECK_INTERVAL + random.randint(1, 4)
                print(f" [✓] {time.strftime('%H:%M:%S')} | Trạng thái: Trong game (Xanh lá). Kiểm tra lại sau {random_delay}s")
                time.sleep(random_delay)
        except KeyboardInterrupt:
            print("\n[-] Đã dừng chạy Rejoin.")
            input("Bấm Enter để quay lại Menu chính...")
            break

def main():
    global USE_ROOT
    while True:
        clear_screen()
        show_banner()
        print(" [1] Setup cấu hình ID / Link Server VIP")
        print(f" [2] Kích hoạt chạy Auto Rejoin (ROOT: {'BẬT' if USE_ROOT else 'TẮT'})")
        print(f" [3] Bật/Tắt chế độ ROOT (Hiện tại: {'ROOT' if USE_ROOT else 'THƯỜNG'})")
        print(" [0] Thoát Tool TinHub")
        print("==================================================")
        choice = input(" -> Chọn chế độ (0-3): ").strip()
        
        if choice == "1":
            clear_screen()
            show_banner()
            global USER_ID, GAME_TARGET, CHECK_INTERVAL
            u = input(f" -> Nhập ID Roblox ({USER_ID}): ").strip()
            if u: USER_ID = u
            g = input(f" -> Nhập ID Map/Link VIP ({GAME_TARGET}): ").strip()
            if g: GAME_TARGET = g
            t = input(f" -> Chu kỳ quét ({CHECK_INTERVAL}s): ").strip()
            if t: CHECK_INTERVAL = int(t)
        elif choice == "2":
            run_rejoin()
        elif choice == "3":
            USE_ROOT = not USE_ROOT
            print(f"\n[+] Đã chuyển sang chế độ: {'ROOT' if USE_ROOT else 'THƯỜNG'}")
            time.sleep(1)
        elif choice == "0":
            sys.exit()

if __name__ == "__main__":
    main()
EOF
