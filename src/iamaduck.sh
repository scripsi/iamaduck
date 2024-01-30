# This is the startup script called by 
# 
#  /etc/systemd/system/iamaduck.service

# *** DEFAULT VARIABLES ***
VPYTHON=".venv/bin/python"
CONFDIR="/mnt/iamaduck"
DBGFILE="$CONFDIR"/startup.log
DBGTTY="/dev/ttyAMA0"
SCRIPT=$(basename "$0")

function dbg {
  echo "$SCRIPT: $1" | tee -a "$DBGFILE" > "$DBGTTY"
}

if [ -e "$DBGFILE" ]
then
  mv -f "$DBGFILE" "$DBGFILE".old
  touch "$DBGFILE"
fi

right_now=$(date)
dbg "Starting! $right_now"

# check if network config has been updated
if [ "$CONFDIR"/wifi.ini -nt /etc/wpa_supplicant/wpa_supplicant.conf ]
then
  dbg "Updated WiFi config found"
  dbg "Rewriting wpa_supplicant..."
  sudo "$VPYTHON" src/update_wifi.py
  # make wifi.ini times match wpa_supplicant.conf to avoid reboot loop
  touch --reference=/etc/wpa_supplicant/wpa_supplicant.conf "$CONFDIR"/wifi.ini
  dbg "wpa_supplicant.conf rewritten. Rebooting... "
  sudo reboot
else
  dbg "No updates to WiFi config found"
fi

# Test network
NETWORK_RETRY=1
NETWORK_RETRY_COUNT=0
NETWORK="OFFLINE"
dbg "Waiting for network..."
while [ $NETWORK_RETRY -gt 0 ]
do
  wget -q --spider https://github.com

  if [ $? -eq 0 ]
  then
    dbg "Internet is up"
    NETWORK_RETRY=0
    NETWORK="ONLINE"
  else
    if [ $NETWORK_RETRY_COUNT -gt 10 ]
    then
      dbg "Internet offline. Too many retries"
    else
      dbg "Internet offline. Retrying in 10 seconds..."
      sleep 10
    fi
  fi
done

dbg "Network is $NETWORK"

# Check for updates
if [ $NETWORK = "ONLINE" ]
then
  dbg "Checking for software updates..."
  git fetch
  updates=$(git rev-list HEAD...origin/main --count)
  if [ $updates -gt 0 ]
  then
    dbg "Software is $updates updates behind current version. Updating..."
    git pull
  else
    dbg "Software is up to date"
  fi
  # Download mail
  dbg "Downloading mail..."
  offlineimap -c "$CONFDIR"/mail.ini
  
fi
dbg "Starting iamaduck.py..."
"$VPYTHON" src/iamaduck.py
