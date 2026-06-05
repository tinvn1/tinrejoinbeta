import os
import time
import requests
import json

# Đường dẫn lưu file cấu hình cố định tại thư mục Download của điện thoại
CONFIG_FILE = "/sdcard/Download/config_rejoin.json"

STATUS_MAP = {
    0: "OFFLINE 🔴",
    1: "ONLINE (Chỉ lướt Web) 🌐",
    2: "IN-GAME (Đang chơi game) 🎮",
    3: "IN STUDIO 🛠️"
}

def load_or_create_config():
    # Kiểm tra xem đã có file cấu hình lưu trong mục Download chưa
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                required_keys = ["user_id", "place_id", "vip_link", "check_interval", "force_interval"]
                if all(key in config for key in required_keys):
                    print("[⚙️] Đã tự động tải cấu hình cũ từ Download/config_rejoin.json")
                    return config
        except:
            print("[⚠️] File cấu hình bị lỗi hoặc chưa đúng định dạng, tiến hành tạo mới...")

    # Giao diện nhập thông tin nếu chưa có file cấu hình lưu trữ
    print("="*50)
    print("   THIẾT LẬP CẤU HÌNH TOOL LẦN ĐẦU (SẼ LƯU VÀO DOWNLOAD)   ")
    print("="*50)
    user_id = int(input("1. Nhập ID Profile cần check (Ví dụ: 312148668): ").strip())
    place_id = input("2. Nhập ID Game (Ví dụ: 90148635862803): ").strip()
    vip_link = input("3. Dán Link Server VIP (https://www.roblox.com/share...): ").strip()
    check_interval = int(input("4. Nhập số giây giãn cách mỗi lần check (Ví dụ: 15): ").strip())
    force_interval = int(input("5. Sau bao nhiêu phút thì ÉP REJOIN 1 lần (Ví dụ: 60): ").strip())

    config = {
        "user_id": user_id,
        "place_id": place_id,
        "vip_link": vip_link,
        "check_interval": check_interval,
        "force_interval": force_interval
    }

    # Tiến hành lưu file cấu hình thẳng ra mục Download của máy
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print("[💾] Đã lưu trữ cấu hình thành công vào thư mục Download!")
    except Exception as e:
        print(f"[❌] Không thể lưu file cấu hình do thiếu quyền bộ nhớ: {e}")
        
    print("="*50)
    return config

def check_roblox_presence(user_id):
    url = "https://presence.roblox.com/v1/presence/users"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"userIds": [user_id]}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data and "userPresences" in data and len(data["userPresences"]) > 0:
                return data["userPresences"][0].get("userPresenceType", 0)
    except:
        pass
    return 0 

def kill_and_launch_roblox(vip_url):
    print("[💥] Đang tiến hành KILL ROBLOX (Tắt tận gốc ứng dụng chạy ngầm)...")
    os.system("am force-stop com.roblox.client")
    time.sleep(2) 
    
    print("[🚀] Đang kích hoạt mở lại Server VIP...")
    os.system(f"am start -a android.intent.action.VIEW -d '{vip_url}'")

def main():
    config = load_or_create_config()
    
    USER_ID = config["user_id"]
    VIP_LINK = config["vip_link"]
    check_interval = config["check_interval"]
    force_interval = config["force_interval"]

    print("\n" + "="*50)
    print("   TOOL REJOIN: AUTO KILL ROBLOX + ÉP REJOIN ĐỊNH KỲ   ")
    print(f"   Target User ID: {USER_ID}")
    print(f"   Thời gian check: {check_interval}s | Ép Rejoin mỗi: {force_interval} phút")
    print("   💡 Mẹo: Để đổi cấu hình mới, hãy xóa file config_rejoin.json trong mục Download đi nhé.")
    print("="*50)
    
    force_timeout = force_interval * 60
    start_time = time.time()
    
    print("\n[+] Tool đang chạy ngầm...")
    print("="*50)
    
    while True:
        try:
            current_time_now = time.time()
            elapsed_time = current_time_now - start_time
            
            # --- CƠ CHẾ 1: ÉP REJOIN BẮT BUỘC THEO ĐỊNH KỲ ---
            if elapsed_time >= force_timeout:
                print(f"\n[🔥] ĐÃ ĐẾN HẸN ÉP REJOIN ĐỊNH KỲ ({force_interval} phút)!")
                kill_and_launch_roblox(VIP_LINK)
                print("[~] Đang chờ 45 giây cho game khởi động lại...")
                time.sleep(45)
                start_time = time.time()
                continue
                
            # --- CƠ CHẾ 2: CHECK TRẠNG THÁI IN-GAME LIÊN TỤC ---
            status = check_roblox_presence(USER_ID)
            status_text = STATUS_MAP.get(status, "KHÔNG RÕ")
            time_str = time.strftime("%H:%M:%S", time.localtime())
            
            time_left = int(force_timeout - elapsed_time)
            print(f"[{time_str}] Trạng thái: {status_text} | Tự động Kill & Rejoin sau: {time_left}s")
            
            # Nếu phát hiện acc mất trạng thái In-Game 🎮 (Xanh lá tay cầm)
            if status != 2:
                print("[⚠️] Phát hiện acc văng trận/offline!")
                kill_and_launch_roblox(VIP_LINK)
                print("[~] Đang chờ 45 giây cho game load xong...")
                time.sleep(45)
            else:
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n[-] Đã dừng Tool thành công.")
            break

if __name__ == "__main__":
    main()
