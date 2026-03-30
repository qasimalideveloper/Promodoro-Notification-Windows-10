from winotify import Notification, audio
import time
import subprocess
import os
import sys

reminder = 0
while True:
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

    
    time.sleep(5*60)
