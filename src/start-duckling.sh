# This is the startup script for I am a Duck
# 
# Call it using a systemd unit file:
# 
# --- /etc/systemd/system/duckling.service
#
# [Unit]
# Description=Status Board
# After=network.target
#
# [Service]
# ExecStart=/bin/bash /mnt/iamaduck/src/start-duckling.sh
# Restart=always
#
# [Install]
# WantedBy=multi-user.target
# ---
#
# sudo systemctl enable duckling.service
