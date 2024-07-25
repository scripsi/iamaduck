import configparser
import subprocess

config=configparser.ConfigParser()
config.read('/mnt/iamaduck/wifi.ini')
networklist=[config['network1'],config['network2'],config['network3'],config['network4'],config['network5']]
for c in networklist:
  if c['ssid']:
    result = subprocess.run(['sudo', 'nmcli', '-t', 'connection', 'show', c['ssid'].strip('"')])
    if result.returncode:
      subprocess.run(['sudo', 'nmcli', 'connection', 'add',
                      'save', 'yes',
                      'type', 'wifi',
                      'con-name', c['ssid'].strip('"'),
                      'ssid', c['ssid'].strip('"')])
    subprocess.run(['sudo', 'nmcli', 'connection',
                    'modify', c['ssid'].strip('"'),
                    'wifi.ssid', c['ssid'].strip('"'),
                    'wifi-sec.key-mgmt', 'wpa-psk',
                    'wifi-sec.psk', c['key'].strip('"')])
                      
