def change_language():
    global current_lang
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        tty.setcbreak(fd)
        enable_mouse()
        
        selected = False
        while not selected:
            Banner()
            print("\033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
            print("\033[1;36m│\033[0m            🌐  SELECT LANGUAGE / NGÔN NGỮ            \033[1;36m│\033[0m")
            print("\033[1;36m└─────────────────────────────────────────────────────┘\033[0m\n")
            
            # Khung nút bấm Tiếng Việt (Khoảng dòng 11 - 13)
            print("  \033[1;42;37m  [1] 🇻🇳 TIẾNG VIỆT (VNI)  -  CHẠM VÀO ĐÂY  \033[0m\n")
            
            # Khung nút bấm English (Khoảng dòng 14 - 16)
            print("  \033[1;44;37m  [2] 🇬🇧 ENGLISH (ENG)     -  TAP HERE TO CHOOSE  \033[0m\n")
            
            # Nút Quay lại
            print("  \033[1;41;37m  [0] ↩️  BACK / QUAY LẠI    \033[0m\n")
            print("\033[1;33m👉 Chạm trực tiếp vào khung nút hoặc bấm phím 1, 2, 0\033[0m")

            # Đọc sự kiện
            evt = read_input_event()
            if evt:
                kind = evt[0]
                if kind == "TOUCH":
                    y = evt[2]
                    # Nhận diện vùng chạm linh hoạt (Cho phép sai số +-1 dòng)
                    if 10 <= y <= 12:
                        current_lang = "VNI"
                        selected = True
                    elif 13 <= y <= 15:
                        current_lang = "ENG"
                        selected = True
                    elif 16 <= y <= 18:
                        selected = True  # Hủy / Quay lại
                        
                elif kind == "KEY":
                    key = evt[1]
                    if key == '1':
                        current_lang = "VNI"
                        selected = True
                    elif key == '2':
                        current_lang = "ENG"
                        selected = True
                    elif key in ['0', '\x1b']: # Phím 0 hoặc ESC
                        selected = True
                        
            time.sleep(0.05)
            
    finally:
        disable_mouse()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    # Lưu cấu hình ngôn ngữ mới vào file JSON
    cfg = load_config()
    cfg["lang"] = current_lang
    save_config(cfg)
    
    print(f"\n\033[1;32m[✅] Language set to: {current_lang}\033[0m")
    time.sleep(1)
