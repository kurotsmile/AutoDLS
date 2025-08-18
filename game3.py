import os
import time
import subprocess
import numpy as np
import threading
import tkinter as tk
import random
import cv2
from tkinter import messagebox
from PIL import Image, ImageTk


# === CẤU HÌNH ===
TAP_DELAY = 3
running = False
adb_path = os.path.join(os.getcwd(), "adb.exe")
scrcpy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scrcpy.exe")
LDPLAYER_PATH = r"F:\LDPlayer\LDPlayer9\dnplayer.exe"
m_right = False

def send_key_to_ldplayer(key):
    subprocess.run(['nircmd', 'win', 'activate', 'ititle', 'LDPlayer'])
    time.sleep(0.2)  # chờ LDPlayer focus
    hold_time = random.uniform(4, 12)  # random từ 2 đến 3 giây
    subprocess.run(["nircmd", "sendkeypress", "down", key])
    time.sleep(hold_time)
    subprocess.run(["nircmd", "sendkeypress", "up", key])

def start_emulator():
    update_status("🔄 Đang khởi động giả lập...")
    subprocess.Popen([LDPLAYER_PATH])
    time.sleep(15)

def open_game():
    update_status("🎮 Đang mở game Dream League Soccer...")
    os.system('adb shell monkey -p com.firsttouchgames.dls7 -c android.intent.category.LAUNCHER 1')
    time.sleep(15)

def tap(x, y):
    subprocess.run([adb_path, "shell", "input", "tap", str(x), str(y)])

def swipe(x1, y1, x2, y2, duration_ms):
    subprocess.run([adb_path, "shell", "input", "swipe",str(x1), str(y1), str(x2), str(y2), str(duration_ms)], check=True)
    time.sleep(1)

def open_match():
    time.sleep(20)
    update_status("⚽ Đang vào chế độ Career...")
    tap(300, 210)
    time.sleep(3)
    update_status("⚽ Đang vào chế độ Academy division...")
    tap(300, 210)
    time.sleep(5)
    update_status("💙 Bấm play")
    tap(1112, 679)
    time.sleep(5)
    update_status("💙 Bỏ qua quảng cáo")
    tap(300, 300)
    time.sleep(3)

def run_loop():
    global running
    if running:
        player_random_act()
        root.after(random.randint(100,2000), run_loop) 

def auto_play():
    global running
    running=True
    update_status("🚕 Tự động chơi")
    run_loop()

def player_random_act():
    if m_right:
        random.choice([player_go_left, player_go_left,player_go_up,player_go_down, player_go_left,player_go_left])()
    else:
        random.choice([player_go_right, player_go_right,player_go_up,player_go_down, player_go_right,player_go_right])()
        

def player_go_right():
    update_status("⚽ Di chuyển trái")
    t1 = threading.Thread(target=lambda: swipe(300, 513, 500, 513, 2200))
    t2 = threading.Thread(target=player_random_Kick)
    t1.start()
    t2.start()
    time.sleep(1)

def player_go_left():
    update_status("⚽ Di chuyển phải")
    t1 = threading.Thread(target=lambda: swipe(271, 500, 140, 500, 2200))
    t2 = threading.Thread(target=player_random_Kick)
    t1.start()
    t2.start()
    time.sleep(1)

def player_go_up():
    update_status("⚽ Di chuyển lên")
    t1 = threading.Thread(target=lambda: swipe(271, 500, 271, 360, 2200))
    t2 = threading.Thread(target=player_random_Kick)
    t1.start()
    t2.start()
    time.sleep(1)

def player_go_down():
    update_status("⚽ Di chuyển xuống")
    t1 = threading.Thread(target=lambda: swipe(271, 500, 271, 627, 2200))
    t2 = threading.Thread(target=player_random_Kick)
    t1.start()
    t2.start()
    time.sleep(1)

def player_go_presure():
    update_status("⚽ player_go_presure")
    send_key_to_ldplayer("K")
    time.sleep(1)

def player_go_hardKick():
    update_status("⚽ player_go_hardKick")
    send_key_to_ldplayer("L")
    time.sleep(1)

def player_random_Kick():
    random.choice([player_go_presure, player_go_hardKick])()
# === GUI ===

def update_status(text):
    status_label.config(text=text)
    root.update()

def start_process():
    global running
    running = True
    threading.Thread(target=full_run, daemon=True).start()

def stop_process():
    global running
    running = False
    update_status("⛔ Đang dừng...")

def full_run():
    try:
        open_game()
        open_match()
        run_loop()
    except Exception as e:
        update_status(f"❌ Lỗi: {e}")
        messagebox.showerror("Lỗi", str(e))

def load_minimap():
    try:
        im = Image.open("minimap.png")
        imgtk = ImageTk.PhotoImage(im)

        map_label.config(image=imgtk)
        map_label.image = imgtk  
    except Exception as e:
        print("❌ Không load được minimap.png:", e)

def test():
    global m_right
    subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=open("screen.png", "wb"))
    img = cv2.imread("screen.png")
    if img is None:
        print("❌ Không load được ảnh screen.png")
        return

    print("Ảnh gốc:", img.shape) 

    # crop minimap
    x, y, w, h = 550, 550, 180, 120   # ví dụ
    minimap = img[y:y+h, x:x+w]

    if minimap.size == 0:
        print("❌ Crop minimap sai tọa độ!")
        return
    else:
        cv2.imwrite("minimap.png", minimap)   # lưu minimap
        print("✅ Đã lưu minimap.png")
        load_minimap()

    print("Minimap:", minimap.shape)

    # chỉ khi chắc chắn minimap có dữ liệu mới chuyển HSV
    hsv = cv2.cvtColor(minimap, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = cv2.bitwise_or(mask1, mask2)
    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Đếm số lượng điểm đỏ bên phải
    total_red = 0
    right_red = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        total_red += 1
        if x > (180/2):
            right_red += 1
        print("Player Red:", x, y)

    # Kiểm tra đa số
    if total_red > 0 and right_red > total_red/2:
        m_right = True

    print("Tổng đỏ:", total_red, "| Bên phải:", right_red, "| m_right =", m_right)

    mask_ball = cv2.inRange(hsv, np.array([0,0,200]), np.array([180,30,255]))
    contours,_ = cv2.findContours(mask_ball, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        print("Ball:", x, y)
   
# === KHỞI TẠO GUI ===

root = tk.Tk()
root.title("🎮 Auto DLS Controller")
root.geometry("500x500")

start_emulator_btn = tk.Button(root, text="▶️ Mở trình giả lập dnplayer", font=("Arial", 14), width=30, command=start_emulator)
start_emulator_btn.pack(pady=10)

start_button = tk.Button(root, text="🚀 Start Game", font=("Arial", 14), width=15, command=start_process)
start_button.pack(pady=5)

start_button = tk.Button(root, text="🚲 Auto Play", font=("Arial", 13), width=15, command=auto_play)
start_button.pack(pady=5)

start_button = tk.Button(root, text="🧭 Check Map", font=("Arial", 13), width=15, command=test)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="⏹ Stop", font=("Arial", 14), width=10, command=stop_process)
stop_button.pack(pady=5)

status_label = tk.Label(root, text="🔍 Chờ bắt đầu...", font=("Arial", 12))
status_label.pack(pady=20)

map_label = tk.Label(root)
map_label.pack()

root.mainloop()
