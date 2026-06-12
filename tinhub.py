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
    print("    ╚═╝   ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ")
    print("\033[1;32m")
    print("="*55)
    print("   🚀 TINHUB REJOIN SYSTEM AUTOMATION (ROOT MODE) 🚀   ")
    print("="*55)
    print("\033[0m")

def setup_new_config():
    Banner()
    print("\033[1;33m[⚙️] KHỞI TẠO / SỬA CẤU HÌNH HỆ THỐNG\033[0m\n")
    
    try:
        user_id = int(input("\033[1;32m[1] Nhập ID Profile cần check (Ví dụ: 312148668):\033[0m ").strip())
        place_id = input("\033[1;32m[2] Nhập ID Game (Ví dụ: 90148635862803):\033[0m ").strip()
        
        print("\033[1;32m[3] Nhập Link Server VIP (Nhấn ENTER để bỏ qua vì đang dùng chế độ mở thường):\033[0m")
        vip_link = input("    => Link: ").strip()
        
        check_interval = int(input("\033[1;32m[4] Nhập số giây giãn cách kiểm tra (Ví dụ: 15):\033[0m ").strip())
        force_interval = int(input("\033[1;32m[5] Sau bao nhiêu phút thì ÉP REJOIN 1 lần (Ví dụ: 60):\033[0m ").strip())
    except ValueError:
        print("\n\033[1;31m[❌] Dữ liệu nhập sai định dạng! Vui lòng setup lại.\033[0m")
        time.sleep(2)
        return None

    config = {
        "user_id": user_id,
        "place_id": place_id,
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
        print("\n\033[1;32m[🗑️] Đã xóa file cấu hình cũ thành công!\033[0m")
    else:
        print("\n\033[1;33m[ℹ️] Không tìm thấy file cấu hình nào để xóa.\033[0m")
    time.sleep(2)

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

def kill_and_launch_roblox():
    print("\n\033[1;31m[🛡️/💥] ROOT: Đang thực hiện BUỘC DỪNG ứng dụng Roblox...\033[0m")
    # Sử dụng lệnh su -c để mượn quyền Root tối cao ép đóng ứng dụng triệt để, khắc phục lỗi phân quyền
    os.system("su -c 'am force-stop com.vng.roblox'")
    os.system("su -c 'am force-stop com.roblox.client'")
    time.sleep(2) 
    
    print("\033[1;34m[🚀] Đang kích hoạt mở lại ứng dụng theo cách thông thường...\033[0m")
    # Mở ứng dụng bình thường qua MainActivity bằng quyền thường (hoặc root để đảm bảo 100% thành công)
    # Thử mở bản Roblox VN trước
    launch_status = os.system("am start -n com.vng.roblox/com.roblox.client.MainActivity > /dev/null 2>&1")
    
    # Nếu không tìm thấy hoặc lỗi bản VN, tự động gọi mở giao diện chính bản Quốc Tế
    if launch_status != 0:
        print("\033[1;33m[ℹ️] Đang kiểm tra và khởi động ứng dụng bản Quốc Tế...\033[0m")
        os.system("am start -n com.roblox.client/com.roblox.client.MainActivity > /dev/null 2>&1")

def run_tool(config):
    Banner()
    USER_ID = config["user_id"]
    PLACE_ID = config["place_id"]
    check_interval = config["check_interval"]
    force_interval = config["force_interval"]

    print("\033[1;35m[▶️] TOOL ĐANG HOẠT ĐỘNG NGẦM (CHẾ ĐỘ ROOT)...\033[0m")
    print(f"Target User ID: {USER_ID} | Game ID: {PLACE_ID}")
    print("\033[1;32mCơ chế: BUỘC DỪNG BẰNG ROOT 🛡️  & MỞ APP THƯỜNG KHÔNG QUA WEB 📱\033[0m")
    print(f"Thời gian quét: {check_interval}s | Vòng lặp ép mở lại: {force_interval} phút")
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
                kill_and_launch_roblox()
                print("[~] Chờ 45 giây cho ứng dụng khởi động vào sảnh chính...")
                time.sleep(45)
                start_time = time.time()
                continue
                
            # 2. KIỂM TRA TRẠNG THÁI ONLINE/IN-GAME
            status = check_roblox_presence(USER_ID)
            status_text = STATUS_MAP.get(status, "KHÔNG RÕ")
            time_str = time.strftime("%H:%M:%S", time.localtime())
            time_left = int(force_timeout - elapsed_time)
            
            print(f"[{time_str}] Status: {status_text} | Tự động Buộc dừng & Rejoin sau: {time_left}s")
            
            if status != 2:
                print("\033[1;31m[⚠️] Phát hiện acc văng trận/offline!\033[0m")
                kill_and_launch_roblox()
                print("[~] Chờ 45 giây cho game load xong ứng dụng...")
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
        print(" \033[1;36m[1]\033[0m Khởi động Tool Rejoin (Chạy luôn)")
        print(" \033[1;36m[2]\033[0m Cài đặt / Sửa thông số cấu hình Tool")
        print(" \033[1;36m[3]\033[0m Xóa cấu hình hiện tại")
        print(" \033[1;31m[0]\033[0m Thoát hệ thống")
        print("="*55)
        
        if os.path.exists(CONFIG_FILE):
            print("\033[1;32m[ℹ️] Đã tìm thấy file cấu hình lưu sẵn trong máy. Bấm [1] để chạy ngay.\033[0m")
        else:
            print("\033[1;33m[⚠️] Chưa có cấu hình trong máy. Vui lòng chọn [2] để Setup lần đầu.\033[0m")
        print("="*55)

        choice = input("\033[1;33mNhập số để lựa chọn tác vụ (0-3): \033[0m").strip()
        
        if choice == "1":
            if os.path.exists(CONFIG_FILE):
                try:
                    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                        config = json.load(f)
                    run_tool(config)
                except:
                    print("\n\033[1;31m[❌] File config lỗi, vui lòng chọn [2] để cài đặt lại.\033[0m")
                    time.sleep(2)
            else:
                print("\n\033[1;31m[❌] Lỗi: Chưa có dữ liệu cấu hình! Vui lòng chọn [2] để setup trước.\033[0m")
                time.sleep(2)
                    
        elif choice == "2":
            setup_new_config()
        elif choice == "3":
            delete_config()
        elif choice == "0":
            print("\n👋 Cảm ơn bạn đã sử dụng TINHUB. Hẹn gặp lại!")
            sys.exit()
        else:
            print("\n\033[1;31m[❌] Lựa chọn không hợp lệ, vui lòng chọn lại!\033[0m")
            time.sleep(1)

if __name__ == "__main__":
    main()
