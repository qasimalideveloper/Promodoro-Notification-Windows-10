from winotify import Notification, audio
import time
import subprocess
import os
import sys
import requests



if getattr(sys, 'frozen', False):
    exe_path = sys.executable
else:
    exe_path = os.path.abspath(__file__)

def task_exist():
    task_name = "Pamodaro"
    check_cmd = f'powershell -Command "Try {{ Get-ScheduledTask -TaskName \'{task_name}\' -ErrorAction Stop | Out-Null; exit 0 }} Catch {{ exit 1 }}"'
    return subprocess.call(check_cmd, shell=True) == 0

ps_command = rf'''
$Action = New-ScheduledTaskAction -Execute '"{exe_path}"'
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Principal = New-ScheduledTaskPrincipal -UserId $env:UserName -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName "Pamodaro" -Principal $Principal -Force
'''

def run_powershell(cmd):
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
        creationflags=subprocess.CREATE_NO_WINDOW,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True
    )


reminder = 0
ping = 0
while True:
    if not task_exist():
        run_powershell(ps_command)
    print('reminder '+ str(reminder))
    print('ping '+str(ping))

    if reminder == 4:
        toast = Notification(app_id="Break Reminder",
                        title="Break Time!",
                        msg=task_exist(),
                        duration="short")
        toast.set_audio(audio.Reminder, loop=False)
        toast.show()
        reminder = 0
    else:
        reminder = reminder + 1

    if ping == 1:
        ping = 0
        try:
            requests.get('https://toxicfriendbackend-2.onrender.com/ping')
            print("Pinged successfully!")
        except Exception as e:
            print("Ping failed:", e)
        try:
            requests.get('https://my-backend-sx6w.onrender.com/ping')
            print("Pinged successfully!")
        except Exception as e:
            print("Ping failed:", e)
    else:
        ping = ping + 1



    time.sleep(5*60)
