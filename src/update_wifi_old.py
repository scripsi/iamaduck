import configparser

config=configparser.ConfigParser()
config.read('/mnt/iamaduck/wifi.ini')
content="country=" + config['default']['country'].lower() + "\n"
content=content + "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\n\n" 
networklist=[config['network1'],config['network2'],config['network3'],config['network4'],config['network5']]
for c in networklist:
  if c['ssid']:
    content+="network={\n"
    content+="ssid=" + c['ssid'] + "\n"
    content+="psk=" + c['key'] + "\n"
    content+="}\n\n"
wpa_supplicant_file=open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w')
wpa_supplicant_file.write(content)
wpa_supplicant_file.close()
