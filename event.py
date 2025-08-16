import pyautogui, pygetwindow, time

# ID LDPlayer
DEVICE_ID = "127.0.0.1:5555"

# Độ phân giải LDPlayer (xem trong Settings của LDPlayer -> Advanced -> Resolution)
LD_WIDTH, LD_HEIGHT = 1280, 720

# Tìm cửa sổ LDPlayer
windows = [w for w in pygetwindow.getAllTitles() if "LDPlayer" in w]
if not windows:
    print("❌ Không tìm thấy cửa sổ LDPlayer")
    exit()

ld = pygetwindow.getWindowsWithTitle(windows[0])[0]
print(f"✅ Đã tìm thấy LDPlayer: {ld.title}")
print("👉 Click vào LDPlayer để ghi lại toạ độ (bấm Ctrl+C để dừng)")

try:
    while True:
        x, y = pyautogui.position()
        if ld.left < x < ld.right and ld.top < y < ld.bottom:
            # Tính lại toạ độ trong Android
            x_android = int((x - ld.left) * LD_WIDTH / ld.width)
            y_android = int((y - ld.top) * LD_HEIGHT / ld.height)
            print(f"adb shell input tap {x_android} {y_android}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n🛑 Dừng lại")
