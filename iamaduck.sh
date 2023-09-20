echo "$0 started!" > iamaduck.log

# Test network
wget -q --spider http://google.com

if [ $? -eq 0 ]; then
    echo "Internet online" >> iamaduck.log
else
    echo "Internet offline" >> iamaduck.log
fi
