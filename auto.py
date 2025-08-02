import os
import time
import cv2
import numpy as np
import threading
import tkinter as tk
from tkinter import messagebox

# === CẤU HÌNH ===
LDPLAYER_PATH = r'"C:\LDPlayer\LDPlayer4.0\dnplayer.exe"'  # Đổi đường dẫn đúng
TAP_DELAY = 3
running = False

# === CHỨC NĂNG ĐIỀU KHIỂN ===

def start_emulator():
    update_status("🔄 Đang khởi động giả lập...")
    os.system(f'start {LDPLAYER_PATH}')
    time.sleep(15)

def open_game():
    update_status("🎮 Đang mở game Dream League Soccer...")
    os.system('adb shell monkey -p com.firsttouchgames.dls3 -c android.intent.category.LAUNCHER 1')
    time.sleep(20)

def tap(x, y):
    os.system(f"adb shell input tap {x} {y}")
    time.sleep(TAP_DELAY)

def swipe(x1, y1, x2, y2, duration_ms):
    os.system(f"adb shell input swipe {x1} {y1} {x2} {y2} {duration_ms}")
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
    tap(500, 700)   # CAREER
    tap(500, 900)   # Global Challenge Cup
    tap(1000, 1800) # PLAY

def auto_play():
    global running
    update_status("🚀 Bắt đầu chơi tự động...")
    for _ in range(10):
        if not running:
            update_status("⏹ Đã dừng.")
            return
        swipe(300, 1000, 700, 1000, 200)  # chạy phải
        time.sleep(2)
        tap(900, 1700)  # chuyền
        time.sleep(1)
        if near_goal():
            tap(1000, 1700)  # sút
            update_status("⚽ Sút bóng!")
            break
    update_status("✅ Kết thúc lượt chơi.")

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
        start_emulator()
        open_game()
        open_match()
        auto_play()
    except Exception as e:
        update_status(f"❌ Lỗi: {e}")
        messagebox.showerror("Lỗi", str(e))

# === KHỞI TẠO GUI ===

root = tk.Tk()
root.title("🎮 Auto DLS Controller")
root.geometry("400x200")

start_button = tk.Button(root, text="▶️ Start", font=("Arial", 14), width=10, command=start_process)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="⏹ Stop", font=("Arial", 14), width=10, command=stop_process)
stop_button.pack(pady=5)

status_label = tk.Label(root, text="🔍 Chờ bắt đầu...", font=("Arial", 12))
status_label.pack(pady=20)

root.mainloop()
