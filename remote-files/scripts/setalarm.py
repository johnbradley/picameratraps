# Sets the PiJuice wakeup alarm.
# The PiJuice only has a single alarm setting.
import sys
import datetime
import configparser
import pijuice

ALARMS_INI_PATH = "alarms.ini"

if len(sys.argv) != 2:
   print("Usage: ./scripts/setalarm.py <alarm-name> ")
   print(f" where alarm-name is an alarm specified in {ALARMS_INI_PATH}.")
   sys.exit(1)

try:
    alarm_name = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(ALARMS_INI_PATH)
    if not alarm_name in config.sections():
        print(f"Error: Alarm name '{alarm_name}' is not found in {ALARMS_INI_PATH}.")
        sys.exit(2)
    alarm_props = config[alarm_name]
    alarm_config = {}
    for key in alarm_props:
        if alarm_props[key].isnumeric():
            alarm_config[key] = int(alarm_props[key])
        else:
             alarm_config[key] = alarm_props[key]
except configparser.ParsingError as e:
    print(f"Error: Invalid config in {ALARMS_INI_PATH}")
    raise e

print("Starting.")

if not 'day' in alarm_config:
    alarm_config['day'] = 'EVERY_DAY'
if not 'second' in alarm_config:
    alarm_config['second'] = 0
if not 'minute' in alarm_config and not 'minute_period' in alarm_config:
    alarm_config['minute'] = 0
if not 'hour' in alarm_config:
    alarm_config['hour'] = 0

now = datetime.datetime.now()
print(f"Current time: {now.isoformat()}.")

print("RTC (UTC) time:", pijuice.PiJuice().rtcAlarm.GetTime().get("data"))

pj = pijuice.PiJuice()
print("Battery charge level:", pj.status.GetChargeLevel().get("data"))

print(f"Setting the next alarm {alarm_config}")
pj.rtcAlarm.SetAlarm(alarm_config)

print("Enabling PiJuice Wakeup")
pj.rtcAlarm.SetWakeupEnabled(True)

print("Done.")
