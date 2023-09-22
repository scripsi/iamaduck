# This is the startup script called by 
# 
#  /etc/systemd/system/iamaduck.service


LOGFILE="startup.log"

if [ -e "$LOGFILE" ]
then
  mv -f "$LOGFILE" "$LOGFILE".old
fi

echo "$0 started!" > "$LOGFILE"
date >> "$LOGFILE"

# check if network config has been updated
if [ wifi.ini -nt /etc/wpa_supplicant/wpa_supplicant.conf ]
then
  echo "Updated WiFi config found" >> "$LOGFILE"
  echo "Rewriting wpa_supplicant..." >> "$LOGFILE"
  sudo python src/update_wifi.py
  # make wifi.ini times match wpa_supplicant.conf to avoid reboot loop
  touch --reference=/etc/wpa_supplicant/wpa_supplicant.conf wifi.ini
  echo "wpa_supplicant.conf rewritten. Rebooting... " >> "$LOGFILE"
  sudo reboot
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
    echo "Internet offline. Retrying in 10s..." >> "$LOGFILE"
    if [ $NETWORK_RETRY_COUNT -gt 10 ]
    then
      echo "Too many retries" >> "$LOGFILE"
    else
      echo "Retrying in 10 seconds..."
      sleep 10
    fi
  fi
done

echo "Network is" $NETWORK >> "$LOGFILE"

# Check for updates
if [ $NETWORK = "ONLINE" ]
then
  echo "Checking for updates..." >> "$LOGFILE"
  git fetch
  updates=$(git rev-list HEAD...origin/main --count)
  if [ $updates -gt 0 ]
  then
    echo "Software is" $updates "updates behind current version. Updating..." >> "$LOGFILE"
    git pull
  else
    echo "Software is up to date" >> "$LOGFILE"
  fi
  # Download mail
  echo "Downloading mail..." >> "$LOGFILE"
  offlineimap -c mail.ini
  
fi
echo "Starting iamaduck.py..." >> "$LOGFILE"
python src/iamaduck.py
