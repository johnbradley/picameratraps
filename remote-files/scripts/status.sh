set -e

echo "> PiJuice Status"
python3 -c 'import pijuice; print(pijuice.PiJuice().status.GetStatus())'
echo ""

echo "> Battery charge level percentage"
python3 -c 'import pijuice; print(pijuice.PiJuice().status.GetChargeLevel().get("data"))'
echo ""

echo "> Remote system date/time"
date
echo ""

echo "> Remote RTC Time (UTC)"
python3 -c 'import pijuice; print(pijuice.PiJuice().rtcAlarm.GetTime().get("data"))'
echo ""

echo "> Alarm setting (UTC)"
python3 -c 'import pijuice; print(pijuice.PiJuice().rtcAlarm.GetAlarm().get("data"))'
echo ""

echo "> Disk usage"
df .
echo ""

echo "> Number of images"
ls images/ | wc -l
echo ""

echo "> Crontab"
crontab -l
echo ""