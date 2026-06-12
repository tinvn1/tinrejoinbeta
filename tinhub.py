import os
import time
import requests
import json
import sys

# Đường dẫn lưu file cấu hình tại thư mục Download
CONFIG_FILE = "/sdcard/Download/config_rejoin.json"

STATUS_MAP = {
    0: "OFFLINE 🔴",
    1: "ONLINE (Chỉ lướt Web) 🌐",
    2: "IN-GAME (Đang chơi game) 🎮",
    3: "IN STUDIO 🛠️"
}

def Banner():
    os.system("clear")
    print("\033[1;36m")
    print(" ████████╗██╗███╗   ██╗██╗  ██╗██╗   ██╗██████╗ ")
    print(" ╚══██╔══╝██║████╗  ██║██║  ██║██║   ██║██╔══██╗")
    print("    ██║   ██║██╔██╗ ██║███████║██║   ██║██████╔╝")
    print("    ██║   ██║██║╚██╗██║██╔══██║██║   ██║██╔══██╗")
    print("    ██║   ██║██║ ╚████║██║  ██║╚██████╔╝██████╔╝")
    print("    ╚═╝   ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ vn ")
    print("\033[1;32m")
    print("="*55)
    print("      🚀 TINHUB REJOIN SYSTEM AUTOMATION (WEB COOKIE) 🚀     ")
    print("="*55)
    print("\033[0m")

def setup_new_config():
    Banner()
    print("\033[1;33m[⚙️] KHỞI TẠO CẤU HÌNH CHECK WEB COOKIE\033[0m\n")
    
    try:
        user_id = int(input("\033[1;32m[1] Nhập ID Profile cần theo dõi (Ví dụ: 312148668):\033[0m ").strip())
        place_id = input("\033[1;32m[2] Nhập ID Game (Ví dụ: 90148635862803):\033[0m ").strip()
        
        print("\033[1;32m[3] Nhập Cookie Roblox (.ROBLOSECURITY) để check Web:\033[0m")
        cookie = input("    => Cookie: ").strip()
        
        print("\033[1;32m[4] Nhập Link Server VIP (Nếu chơi Server Thường, nhấn ENTER bỏ qua):\033[0m")
        vip_link = input("    => Link VIP: ").strip()
        
        check_interval = int(input("\033[1;32m[5] Nhập số giây giãn cách kiểm tra (Ví dụ: 15):\033[0m ").strip())
        force_interval = int(input("\033[1;32m[6] Sau bao nhiêu phút thì ÉP REJOIN định kỳ (Ví dụ: 60):\033[0m ").strip())
    except ValueError:
        print("\n\033[1;31m[❌] Dữ liệu nhập sai định dạng! Vui lòng thiết lập lại.\033[0m")
        time.sleep(2)
        return None

    config = {
        "user_id": user_id,
        "place_id": place_id,
        "cookie": cookie,
        "vip_link": vip_link,
        "check_interval": check_interval,
        "force_interval": force_interval
    }

    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print("\n\033[1;32m[💾] Đã lưu cấu hình an toàn vào thư mục Download!\033[0m")
    except Exception as e:
        print(f"\n\033[1;31m[❌] Lỗi lưu file: {e}\033[0m")
    
    time.sleep(2)
    return config

def delete_config():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print("\n\033[1;32m[🗑️] Đã xóa file cấu hình thành công!\033[0m")
    else:
        print("\n\033[1;33m[ℹ️] Không tìm thấy file cấu hình để xóa.\033[0m")
    time.sleep(2)

def check_roblox_presence_web(user_id, cookie_str):
    url = "https://presence.roblox.com/v1/presence/users"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    # Nạp cookie định dạng chuẩn của hệ thống Web Roblox
    cookies = {".ROBLOSECURITY": cookie_str}
    payload = {"userIds": [user_id]}
    
    try:
        response = requests.post(url, json=payload, headers=headers, cookies=cookies, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and "userPresences" in data and len(data["userPresences"]) > 0:
                return data["userPresences"][0].get("userPresenceType", 0)
    except Exception as e:
        print(f"\n\033[1;31m[⚠️] Lỗi kết nối Web Roblox: {e}\033[0m")
    return 0 

def kill_and_launch_roblox(place_id, vip_url):
    print("\n\033[1;31m[🛡️/💥] ROOT: Đang thực hiện BUỘC DỪNG ứng dụng Roblox...\033[0m")
    # Sử dụng quyền Root tối cao để Force Stop sạch sẽ cả bản VNG lẫn Quốc Tế
    os.system("su -c 'am force-stop com.vng.roblox'")
    os.system("su -c 'am force-stop com.roblox.client'")
    time.sleep(2.5) 
    
    # Thiết lập đường link Intent để thả vào game
    if vip_url and vip_url.startswith("http"):
        print("\033[1;34m[🔗] Đang thả link điều hướng Server VIP...\033[0m")
        intent_url = vip_url
    else:
        print(f"\033[1;34m[🔗] Đang thả link điều hướng vào thẳng Game ID: {place_id}...\033[0m")
        intent_url = f"roblox://placeId={place_id}"
        
    # Thả link trực tiếp bằng quyền Root vào bản VNG trước
    print("\033[1;32m[🚀] Đang đẩy lệnh nạp map vào Roblox VN...\033[0m")
    launch_status = os.system(f"su -c 'am start -p com.vng.roblox -a android.intent.action.VIEW -d \"{intent_url}\"' > /dev/null 2>&1")
    
    # Nếu không có bản VNG, tự động đẩy link sang mở bản Quốc Tế
    if launch_status != 0:
        print("\033[1;33m[ℹ️] Chuyển hướng đẩy link sang mở bản Quốc Tế...\033[0m")
        os.system(f"su -c 'am start -p com.roblox.client -a android.intent.action.VIEW -d \"{intent_url}\"'")

def run_tool(config):
    Banner()
    USER_ID = config["user_id"]
    PLACE_ID = config["place_id"]
    COOKIE = config["cookie"]
    VIP_LINK = config["vip_link"]
    check_interval = config["check_interval"]
    force_interval = config["force_interval"]

    print("\033[1;35m[▶️] TOOL WEB COOKIE REJOIN ĐANG CHẠY NGẦM...\033[0m")
    print(f"Target User ID: {USER_ID} | Game ID: {PLACE_ID}")
    print(f"Chế độ sảnh: " + ("SERVER VIP 💎" if VIP_LINK else "SERVER THƯỜNG 🌐"))
    print("\033[1;32mCơ chế: CHECK TRẠNG THÁI WEB 🌐 | GIẾT BẰNG ROOT 🛡️ | THẢ LINK 🔗\033[0m")
    print("="*55)
    
    force_timeout = force_interval * 60
    start_time = time.time()
    
    while True:
        try:
            current_time_now = time.time()
            elapsed_time = current_time_now - start_time
            
            # 1. ÉP REJOIN ĐỊNH KỲ BẤT KỂ TRẠNG THÁI
            if elapsed_time >= force_timeout:
                print(f"\n\033[1;33m[🔥] ĐÃ ĐẾN HẸN ÉP REJOIN ĐỊNH KỲ ({force_interval} phút)!\033[0m")
                kill_and_launch_roblox(PLACE_ID, VIP_LINK)
                print("[~] Chờ 45 giây cho sảnh game khởi động...")
                time.sleep(45)
                start_time = time.time()
                continue
                
            # 2. CHECK TRẠNG THÁI WEB QUA COOKIE
            status = check_roblox_presence_web(USER_ID, COOKIE)
            status_text = STATUS_MAP.get(status, "KHÔNG RÕ")
            time_str = time.strftime("%H:%M:%S", time.localtime())
            time_left = int(force_timeout - elapsed_time)
            
            print(f"[{time_str}] Web Status: {status_text} | Tự động Ép tắt & Thả link sau: {time_left}s")
            
            if status != 2: # Nếu không phải trạng thái IN-GAME (2)
                print("\033[1;31m[⚠️] Phát hiện acc đã văng trận trên Web!\033[0m")
                kill_and_launch_roblox(PLACE_ID, VIP_LINK)
                print("[~] Chờ 45 giây cho game nạp map mới...")
                time.sleep(45)
            else:
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\033[1;31m[-] Đã tạm dừng tool.\033[0m")
            time.sleep(1.5)
            break

def main():
    while True:
        Banner()
        print("\033[1;32m[ MENU LỰA CHỌN SETTING ]\033[0m")
        print(" \033[1;36m[1]\033[0m Khởi động Tool Rejoin (Check Cookie Web)")
        print(" \033[1;36m[2]\033[0m Cài đặt / Cập nhật cấu hình (Nhập Cookie)")
        print(" \033[1;36m[3]\033[0m Xóa cấu hình hiện tại")
        print(" \033[1;31m[0]\033[0m Thoát")
        print("="*55)
        
        if os.path.exists(CONFIG_FILE):
            print("\033[1;32m[ℹ️] Đã tìm thấy cấu hình cũ. Bấm [1] để chạy ngay.\033[0m")
        else:
            print("\033[1;33m[⚠️] Chưa có cấu hình. Vui lòng chọn [2] để Setup nhập Cookie.\033[0m")
        print("="*55)

        choice = input("\033[1;33mNhập lựa chọn của bạn (0-3): \033[0m").strip()
        
        if choice == "1":
            if os.path.exists(CONFIG_FILE):
                try:
                    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                        config = json.load(f)
                    run_tool(config)
                except:
                    print("\n\033[1;31m[❌] File config lỗi, vui lòng chọn [2] để setup lại.\033[0m")
                    time.sleep(2)
            else:
                print("\n\033[1;31m[❌] Lỗi: Chưa có dữ liệu! Vui lòng chọn [2] để cài đặt trước.\033[0m")
                time.sleep(2)
                    
        elif choice == "2":
            setup_new_config()
        elif choice == "3":
            delete_config()
        elif choice == "0":
            print("\n👋 Cảm ơn bạn đã sử dụng TINHUB. Hẹn gặp lại!")
            sys.exit()
        else:
            print("\n\033[1;31m[❌] Lựa chọn không hợp lệ!\033[0m")
            time.sleep(1)

if __name__ == "__main__":
    main()
