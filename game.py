import os
import time
import cv2
import subprocess
import numpy as np
import threading
import tkinter as tk
import random
import re
from tkinter import messagebox

# === CẤU HÌNH ===
TAP_DELAY = 3
running = False
adb_path = os.path.join(os.getcwd(), "adb.exe")
scrcpy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scrcpy.exe")
LDPLAYER_PATH = r'"C:\LDPlayer\LDPlayer4.0\dnplayer.exe"'

def send_key_to_ldplayer(key):
    subprocess.run(['nircmd', 'win', 'activate', 'ititle', 'LDPlayer'])
    time.sleep(0.2)  # chờ LDPlayer focus
    subprocess.run(['nircmd', 'sendkeypress', key])

def start_emulator():
    update_status("🔄 Đang khởi động giả lập...")
    os.system(f'start {LDPLAYER_PATH}')
    time.sleep(15)

def open_game():
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
        root.after(random.randint(500,3000), run_loop) 

def auto_play():
    global running
    running=True
    update_status("🚕 Tự động chơi")
    run_loop()

def player_random_act():
    random.choice([player_go_right, player_go_left,player_go_up,player_go_down, player_go_left,player_go_right, player_go_left,player_go_right])()

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

def test():
    tap(1149,636)
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

start_button = tk.Button(root, text="🚲 Test", font=("Arial", 13), width=15, command=test)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="⏹ Stop", font=("Arial", 14), width=10, command=stop_process)
stop_button.pack(pady=5)

status_label = tk.Label(root, text="🔍 Chờ bắt đầu...", font=("Arial", 12))
status_label.pack(pady=20)

root.mainloop()
