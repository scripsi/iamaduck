# This is the startup script called by 
# 
#  /etc/systemd/system/iamaduck.service

LOGFILE="iamaduck.log"

echo "$0 started!" > "$LOGFILE"
date >> "$LOGFILE"

# check if network config has been updated
if [ wifi.ini -nt /etc/wpa_supplicant/wpa_supplicant.conf ]
then
  echo "Updated WiFi config found" >> "$LOGFILE"
  echo "Rewriting wpa_supplicant..." >> "$LOGFILE"
  sudo python src/update_wifi.py
  echo "wpa_supplicant.conf rewritten. Rebooting... " >> "$LOGFILE"
  # sudo reboot
else
  echo "No updates to WiFi config found" >> "$LOGFILE"
fi

# Test network
NETWORK_RETRY=1
NETWORK_RETRY_COUNT=0
NETWORK="OFFLINE"
echo "Waiting for network..." >> "$LOGFILE"
while [ $NETWORK_RETRY -gt 0 ]
do
  wget -q --spider https://github.com

  if [ $? -eq 0 ]
  then
    echo "Internet online" >> "$LOGFILE"
    NETWORK_RETRY=0
    NETWORK="ONLINE"
  else
    echo "Internet offline" >> "$LOGFILE"
    if [ $NETWORK_RETRY_COUNT -gt 10 ]
    then
      echo "Too many retries" >> "$LOGFILE"
    else
      echo "Retrying in 10 seconds..."
      sleep 10
    fi
  fi
done

