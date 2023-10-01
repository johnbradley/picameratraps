
import datetime
import time
import subprocess
import pijuice
import sys

RECORD_TIME_SECONDS = 30
RECORD_TIME_MS = RECORD_TIME_SECONDS * 1000
CAPTURE_HOURS = [
    7, 8, 
    11,12,13,
    16,17,18
]
UTC_OFFSET_HR = 4


def is_recording_time():
    current_hour = datetime.datetime.now().hour
    print(f"Current hour is {current_hour}.")
    return current_hour >= 7 and current_hour < 19


def wait_until_start_of_minute():
    print("Waiting for start of next minute")
    while datetime.datetime.now().second != 0:
        time.sleep(0.1)


def run_command(cmd_str):
    print(f"Running {cmd_str}")
    subprocess.run(f"bash -c '{cmd_str}'", shell=True)    


def record_video(now):
    print("Recording video")
    prefix = now.strftime('%Y-%m-%d_%H-%M-%S')
    cmd = f"libcamera-vid -t {RECORD_TIME_MS} -o videos/{prefix}.h264 --save-pts videos/{prefix}.ts.txt --nopreview >> logs/record.log 2>&1"
    run_command(cmd)


def get_next_alarm_hour(current_hour):
    next_alarm_hours = [hr for hr in CAPTURE_HOURS if hr > current_hour]
    if next_alarm_hours:
        return next_alarm_hours[0]
    # the next alarm must be tomorrow
    return CAPTURE_HOURS[0]


def update_alarm(now):
    next_alarm_hour = get_next_alarm_hour(now.hour)
    alarm_config = {
        "day": "EVERY_DAY",
        "hour": next_alarm_hour + UTC_OFFSET_HR,
        "minute_period": 5,
        "second": 0
    }
    pj = pijuice.PiJuice()

    print(f"Setting the next alarm {alarm_config}")
    pj.rtcAlarm.SetAlarm(alarm_config)

    print("Enabling PiJuice Wakeup")
    pj.rtcAlarm.SetWakeupEnabled(True)


def shutdown():
    cmd = "sudo shutdown -h now"
    run_command(cmd)

if len(sys.argv) == 2 and sys.argv[1] == "init":
    print("Setting the alarm")
    now = datetime.datetime.now()
    update_alarm(now)
    print("Shutting down", flush=True)
    shutdown()
else:
    if is_recording_time():
        print("Within recording time range")
        wait_until_start_of_minute()
        now = datetime.datetime.now()
        record_video(now)
        if now.minute >= 55: # end of hour so need to update alarm
            update_alarm(now)
        print("Shutting down", flush=True)
        shutdown()
    else:
        print("Unschedule startup time - Expected that user will be downloading data.")
