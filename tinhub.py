import os
import time
import requests

# === CẤU HÌNH THÔNG SỐ CHUẨN CỦA BẠN ===
USER_ID = 312148668             # ID Profile cần check
PLACE_ID = "90148635862803"     # ID Game chuẩn 14 chữ số (Survive the Apocalypse)
VIP_LINK = "https://www.roblox.com/share?code=4c2ac37f96906a4892f37026c4502184&type=Server"

STATUS_MAP = {
    0: "OFFLINE 🔴",
    1: "ONLINE (Chỉ lướt Web) 🌐",
    2: "IN-GAME (Đang chơi game) 🎮",
    3: "IN STUDIO 🛠️"
}

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

def launch_roblox_vip(vip_url):
    # Sử dụng lệnh mở link qua trình duyệt để kích hoạt app Roblox vào thẳng phòng VIP
    os.system(f"am start -a android.intent.action.VIEW -d '{vip_url}'")

def main():
    print("="*50)
    print("   TOOL SONG SONG: CHECK TRẠNG THÁI + ÉP REJOIN ĐỊNH KỲ   ")
    print(f"   Target User ID: {USER_ID}")
    print("="*50)
    
    check_interval = int(input("Nhập số giây giãn cách mỗi lần check (Ví dụ: 15): "))
    force_interval = int(input("Sau bao nhiêu phút thì ÉP REJOIN 1 lần (Ví dụ: 60): "))
    
    # Quy đổi thời gian ép rejoin từ phút sang giây
    force_timeout = force_interval * 60
    start_time = time.time()
    
    print("\n[+] Tool đang chạy ngầm...")
    print("="*50)
    
    while True:
        try:
            current_time_now = time.time()
            elapsed_time = current_time_now - start_time
            
            # --- CƠ CHẾ 1: ÉP REJOIN BẮT BUỘC THEO ĐỊNH KỲ (Bất kể On hay Off) ---
            if elapsed_time >= force_timeout:
                print(f"\n[🔥] ĐÃ ĐẾN HẸN ÉP REJOIN ({force_interval} phút)! Bất kể có đang On hay không, tiến hành mở lại game...")
                launch_roblox_vip(VIP_LINK)
                print("[~] Đang chờ 45 giây cho game khởi động lại...")
                time.sleep(45)
                start_time = time.time() # Thiết lập lại mốc thời gian đếm ngược mới
                continue
                
            # --- CƠ CHẾ 2: CHECK TRẠNG THÁI XANH LÁ (IN-GAME) LIÊN TỤC ---
            status = check_roblox_presence(USER_ID)
            status_text = STATUS_MAP.get(status, "KHÔNG RÕ")
            time_str = time.strftime("%H:%M:%S", time.localtime())
            
            # Tính thời gian còn lại đến mốc Ép Rejoin bắt buộc tiếp theo
            time_left = int(force_timeout - elapsed_time)
            print(f"[{time_str}] Trạng thái: {status_text} | Tự động Ép Rejoin sau: {time_left}s")
            
            # Nếu phát hiện acc mất trạng thái In-Game 🎮 (Xanh lá tay cầm)
            if status != 2:
                print("[⚠️] Phát hiện acc không ở trong trận! Kích hoạt Rejoin vào Server VIP...")
                launch_roblox_vip(VIP_LINK)
                print("[~] Đang chờ 45 giây cho game ổn định...")
                time.sleep(45)
                # Lưu ý: Không reset start_time ở đây để giữ nguyên lịch hẹn ép Rejoin định kỳ của bạn
            else:
                # Nếu vẫn đang In-game mượt mà, tạm nghỉ theo số giây bạn cài rồi check tiếp
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n[-] Đã dừng Tool thành công.")
            break

if __name__ == "__main__":
    main()
