# Capture video and/or set alarms
import datetime
import time
import subprocess
import pijuice
import sys
import configparser


CAPTURE_INI_PATH = "capture.ini"
config = configparser.ConfigParser()
config.read(CAPTURE_INI_PATH)
settings = config['settings']

RECORD_TIME_SECONDS = int(settings['RECORD_TIME_SECONDS'])
RECORD_TIME_MS = RECORD_TIME_SECONDS * 1000
CAPTURE_HOURS = [int(hr) for hr in settings['CAPTURE_HOURS'].split(',')]
UTC_OFFSET_HR = int(settings['UTC_OFFSET_HR'])
SET_ALARM_AFTER_MINUTE = int(settings['SET_ALARM_AFTER_MINUTE'])
try:
    ALARM_MINUTE_PERIOD = int(settings['ALARM_MINUTE_PERIOD'])
except KeyError:
    ALARM_MINUTE_PERIOD = None
try:
    ALARM_MINUTE = int(settings['ALARM_MINUTE'])
except KeyError:
    ALARM_MINUTE = None
CAPTURE_SCRIPT = settings['CAPTURE_SCRIPT']

if not ALARM_MINUTE_PERIOD and not ALARM_MINUTE:
    print(f"Invalid {CAPTURE_INI_PATH} setting. You must specify ALARM_MINUTE_PERIOD or ALARM_MINUTE ")
    sys.exit(1)


def is_recording_time():
    current_hour = datetime.datetime.now().hour
    print(f"Current hour is {current_hour}.")
    return current_hour in CAPTURE_HOURS


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
    cmd = f"{CAPTURE_SCRIPT} {RECORD_TIME_MS} {prefix}"
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
        "second": 0
    }
    if ALARM_MINUTE_PERIOD:
        alarm_config["minute_period"] = ALARM_MINUTE_PERIOD
    else:
        alarm_config["minute"] = ALARM_MINUTE

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
else:
    if is_recording_time():
        print("Within recording time range")
        wait_until_start_of_minute()
        now = datetime.datetime.now()
        record_video(now)
        if now.minute >= SET_ALARM_AFTER_MINUTE: # end of hour so need to update alarm
            update_alarm(now)
        print("Shutting down", flush=True)
        shutdown()
    else:
        print("Unschedule startup - Assuming user will be downloading data and then shutdown before next alarm.")
