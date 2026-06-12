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
    print("    🚀 TINHUB REJOIN SYSTEM AUTOMATION (ROOT + LINK DETECT) 🚀   ")
    print("="*55)
    print("\033[0m")

def setup_new_config():
    Banner()
    print("\033[1;33m[⚙️] KHỞI TẠO / SỬA CẤU HÌNH HỆ THỐNG\033[0m\n")
    
    try:
        user_id = int(input("\033[1;32m[1] Nhập ID Profile cần check (Ví dụ: 312148668):\033[0m ").strip())
        place_id = input("\033[1;32m[2] Nhập ID Game (Ví dụ: 90148635862803):\033[0m ").strip()
        
        print("\033[1;32m[3] Nhập Link Server VIP (Nếu dùng Server Thường, nhấn ENTER bỏ qua):\033[0m")
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

def kill_and_launch_roblox(place_id, vip_url):
    print("\n\033[1;31m[🛡️/💥] ROOT: Đang thực hiện BUỘC DỪNG ứng dụng Roblox...\033[0m")
    # Sử dụng quyền Root tối cao để ép đóng hoàn toàn ứng dụng chạy ngầm
    os.system("su -c 'am force-stop com.vng.roblox'")
    os.system("su -c 'am force-stop com.roblox.client'")
    time.sleep(2) 
    
    # Thiết lập link điều hướng (Ưu tiên Link VIP, nếu không có sẽ thả link ID Game thường)
    if vip_url and vip_url.startswith("http"):
        print("\033[1;34m[🔗] Cơ chế cũ: Đang thả link điều hướng Server VIP...\033[0m")
        intent_url = vip_url
    else:
        print(f"\033[1;34m[🔗] Cơ chế cũ: Đang thả link điều hướng vào thẳng Game ID: {place_id}...\033[0m")
        intent_url = f"roblox://placeId={place_id}"
        
    # Kích hoạt cơ chế thả link bằng quyền Root để ép hệ thống gọi ứng dụng mở trực tiếp, bỏ qua bước chọn trình duyệt
    # Ưu tiên thả link vào bản Roblox VN trước
    print("\033[1;32m[🚀] Đang đẩy lệnh vào ứng dụng Roblox VN...\033[0m")
    launch_status = os.system(f"su -c 'am start -p com.vng.roblox -a android.intent.action.VIEW -d \"{intent_url}\"' > /dev/null 2>&1")
    
    # Nếu máy không cài bản VN, tự động mượn Root đẩy link trực tiếp sang bản Quốc Tế
    if launch_status != 0:
        print("\033[1;33m[ℹ️] Không tìm thấy bản VNG, đang đẩy lệnh sang mở bản Quốc Tế...\033[0m")
        os.system(f"su -c 'am start -p com.roblox.client -a android.intent.action.VIEW -d \"{intent_url}\"'")

def run_tool(config):
    Banner()
    USER_ID = config["user_id"]
    PLACE_ID = config["place_id"]
    VIP_LINK = config["vip_link"]
    check_interval = config["check_interval"]
    force_interval = config["force_interval"]

    print("\033[1;35m[▶️] TOOL ĐANG HOẠT ĐỘNG NGẦM TRÊN CƠ CHẾ CŨ...\033[0m")
    print(f"Target User ID: {USER_ID} | Game ID: {PLACE_ID}")
    print(f"Chế độ sảnh: " + ("SERVER VIP 💎" if VIP_LINK else "SERVER THƯỜNG 🌐"))
    print("\033[1;32mCơ chế: BUỘC DỪNG BẰNG ROOT 🛡️  & THẢ LINK INTENT VÀO THẲNG MAP 🔗\033[0m")
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
                kill_and_launch_roblox(PLACE_ID, VIP_LINK)
                print("[~] Chờ 45 giây cho ứng dụng load link vào thẳng trận...")
                time.sleep(45)
                start_time = time.time()
                continue
                
            # 2. KIỂM TRA TRẠNG THÁI ONLINE/IN-GAME
            status = check_roblox_presence(USER_ID)
            status_text = STATUS_MAP.get(status, "KHÔNG RÕ")
            time_str = time.strftime("%H:%M:%S", time.localtime())
            time_left = int(force_timeout - elapsed_time)
            
            print(f"[{time_str}] Status: {status_text} | Tự động Buộc dừng & Thả link sau: {time_left}s")
            
            if status != 2:
                print("\033[1;31m[⚠️] Phát hiện acc văng trận/offline!\033[0m")
                kill_and_launch_roblox(PLACE_ID, VIP_LINK)
                print("[~] Chờ 45 giây cho game load xong map...")
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
