#! /usr/bin/env python3

# Замена D:\SCENE\MemorialToucher\EXE\time_check_start.bat
#
# Избавляемся от черного окна .bat процедуры, никогда не вылезет сдуру
#
# Задавить эту процедуру, а вместе с ней Toucher.exe & Blackscreen.exe:
#   * найти в диспетчере задач, процессы... pythonw
#   * задавить его вместе с подзадачами

import subprocess
import time

# --- Время работы терминала ---------

START_ =  "8:55"
END_   = "18:00"

# ------------------------------------

start_  = START_.split(":")
end_    = END_.split(":")
start_  = int(start_[0]) * 60 + int(start_[1])
end_    = int(end_[0])   * 60 + int(end_[1])

while(True):
    time.sleep(10)
    now = time.localtime()
    now = now.tm_hour * 60 + now.tm_min
    if now >=  start_ and now < end_:
        subprocess.call([r'D:\SCENE\MemorialToucher\EXE\toucher.exe', END_])
    else:
        subprocess.call([r'D:\SCENE\BlackScreen\EXE\blackscreen.exe', START_])
