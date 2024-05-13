#!/usr/bin/bash
service_user="ubuntu"

./chainbridge --config config.json --verbosity debug --blockstore . --keystore ./keys --metrics 2>&1 | tee -a ./chainbridge.log
crontab -u $service_user -l ; echo "*/2 * * * * bash ./service_monitoring.sh" | crontab -u $service_user -
~
