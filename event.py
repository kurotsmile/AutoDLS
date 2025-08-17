import subprocess, re

proc = subprocess.Popen(["adb", "shell", "getevent", "-l"], stdout=subprocess.PIPE, text=True)

x = y = None
for line in proc.stdout:
    if "ABS_MT_POSITION_X" in line:
        x = int(line.split()[-1], 16)
    elif "ABS_MT_POSITION_Y" in line:
        y = int(line.split()[-1], 16)
    elif "SYN_REPORT" in line and x is not None and y is not None:
        print(f"Tap tại tọa độ: ({x}, {y})")
        x = y = None
