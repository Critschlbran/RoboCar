hello

Added to /etc/rc.local

service dhcpcd stop
ifconfig wlan0 down
service dhcpcd start

cd /home/pi/work
sudo -u root sh ap.sh &
#************************************#
cd /home/pi/work/wifirobots
sudo -u root sh startwifirobot.sh &

