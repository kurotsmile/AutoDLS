import os
import time
import cv2
import subprocess
import numpy as np
import threading
import tkinter as tk
import random
from tkinter import messagebox

# === CẤU HÌNH ===
TAP_DELAY = 3
running = False
adb_path = os.path.join(os.getcwd(), "adb.exe")
scrcpy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scrcpy.exe")
LDPLAYER_PATH = r'"C:\LDPlayer\LDPlayer4.0\dnplayer.exe"'

def start_emulator():
    update_status("🔄 Đang khởi động giả lập...")
    os.system(f'start {LDPLAYER_PATH}')
    time.sleep(15)

def start_scrcpy_usb():
    try:
        update_status("🔄 Khởi động lại ADB...")
        subprocess.run([adb_path, "kill-server"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([adb_path, "start-server"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        update_status("🔍 Kiểm tra thiết bị USB...")
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")

        if len(lines) <= 1 or not lines[1].strip().endswith("device"):
            update_status("⚠ Không tìm thấy thiết bị USB. Hãy cắm cáp và bật USB Debugging.")
            return

        update_status("🚀 Mở scrcpy...")
        subprocess.Popen([scrcpy_path], shell=True)
        update_status("✅ Scrcpy đã khởi động thành công qua USB.")

    except Exception as e:
        update_status("❌ Lỗi khi khởi động scrcpy:", e)

def open_game():
    update_status("🔌 Đang kết nối điện thoại...")
    os.system('adb devices')
    time.sleep(1)
    update_status("🎮 Đang mở game Dream League Soccer...")
    os.system('adb shell monkey -p com.firsttouchgames.dls7 -c android.intent.category.LAUNCHER 1')
    time.sleep(5)

def tap(x, y):
    subprocess.run([adb_path, "shell", "input", "tap", str(x), str(y)])

def swipe(x1, y1, x2, y2, duration_ms):
    subprocess.run([adb_path, "shell", "input", "swipe",str(x1), str(y1), str(x2), str(y2), str(duration_ms)], check=True)
    time.sleep(1)

def capture_screen():
    os.system("adb shell screencap -p /sdcard/screen.png")
    os.system("adb pull /sdcard/screen.png > nul")

def near_goal():
    capture_screen()
    img = cv2.imread('screen.png')
    if img is None:
        return False
    goal_template = cv2.imread('goal_template.png', 0)
    if goal_template is None:
        update_status("❌ Thiếu file goal_template.png")
        return False
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, goal_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    update_status(f"📷 Mức trùng khung thành: {max_val:.2f}")
    return max_val > 0.7

def open_match():
    update_status("⚽ Đang vào chế độ Career...")
    tap(200, 200) # CAREER
    time.sleep(2)
    update_status("⚽ Đang vào chế độ Academy division...")
    tap(350, 210) # Global Challenge Cup
    time.sleep(2)
    update_status("💙 Bấm play")
    tap(1350, 687) # Global Challenge Cup
    time.sleep(2)
    tap(300, 300)
    time.sleep(3)

def auto_play():
    global running
    update_status("🚀 Bắt đầu chơi tự động...")
    for _ in range(10):
        if not running:
            update_status("⏹ Đã dừng.")
            return
        swipe(300, 513, 700, 513, 200)  # chạy phải
        time.sleep(2)
        tap(900, 1700)  # chuyền
        time.sleep(1)
        if near_goal():
            tap(1000, 1700)  # sút
            update_status("⚽ Sút bóng!")
            break
    update_status("✅ Kết thúc lượt chơi.")

def run_loop():
    global running
    if running:
        player_random_act()
        root.after(5000, run_loop) 

def player_random_act():
    random.choice([player_go_right, player_go_left,player_go_up,player_go_down])()

def player_go_right():
    update_status("⚽ Di chuyển trái")
    swipe(300, 513, 500, 513, 2200)  # chạy phải
    player_random_Kick()
    time.sleep(1)

def player_go_left():
    update_status("⚽ Di chuyển phải")
    swipe(271, 500, 140, 500, 2200)  # chạy trái
    player_random_Kick()
    time.sleep(1)

def player_go_up():
    update_status("⚽ Di chuyển lên")
    swipe(271, 500, 271, 360, 2200)  # chạy lên
    player_random_Kick()
    time.sleep(1)

def player_go_down():
    update_status("⚽ Di chuyển xuống")
    swipe(271, 500, 271, 627, 2200)  # chạy xuống
    player_random_Kick()
    time.sleep(1)

def player_go_presure():
    tap(1184,625)
    time.sleep(1)

def player_go_hardKick():
    tap(1368,625)
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
        #auto_play()
    except Exception as e:
        update_status(f"❌ Lỗi: {e}")
        messagebox.showerror("Lỗi", str(e))

# === KHỞI TẠO GUI ===

root = tk.Tk()
root.title("🎮 Auto DLS Controller")
root.geometry("500x500")

start_emulator_btn = tk.Button(root, text="▶️ Mở trình giả lập dnplayer", font=("Arial", 14), width=30, command=start_emulator)
start_emulator_btn.pack(pady=10)

start_scrcpy_btn = tk.Button(root, text="▶️ Mở trình SCRCPY", font=("Arial", 14), width=20, command=start_scrcpy_usb)
start_scrcpy_btn.pack(pady=5)

start_button = tk.Button(root, text="🚀 Start Game", font=("Arial", 14), width=15, command=start_process)
start_button.pack(pady=5)

start_button = tk.Button(root, text="🚲 Auto Play", font=("Arial", 13), width=15, command=run_loop)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="⏹ Stop", font=("Arial", 14), width=10, command=stop_process)
stop_button.pack(pady=5)

status_label = tk.Label(root, text="🔍 Chờ bắt đầu...", font=("Arial", 12))
status_label.pack(pady=20)

root.mainloop()
