# This script chooses a new random Quack Of The Hour (qoth)
# and then runs offlineimap on motherduck only to upload it

~/iamaduck/.venv/bin/python ~/iamaduck/src/randomqoth.py
offlineimap -c /mnt/iamaduck/mail.ini -k Repository_Remote:readonly=False -f qoth
