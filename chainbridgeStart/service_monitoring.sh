
#!/bin/bash

#This server is owned by ***
service_user="ubuntu"
service="Chainbridge"
service_status=`pgrep -x chainbridge`

# slack variables
slack_webhook="https://hooks.slack.com/services/*****"
# Personal/Bot slack token
slack_token="xoxb-not-a-real-token-this-will-not-work"
# slack user memberId
slack_memberId="*******"
slack_api_url="https://slack.com/api/files.upload"
slack_channel=channel-name
# file variables
service_log_file=./chainbridge.log
service_temp_log_send_file=sendFile.txt

# Checking if the service is runnig or not
if [ "$service_status" > "0" ]
then
    echo "$service service running"
else 
    echo "service not running"
    # when service is not running, sending notification to slack and starting the service
    # member Id
    payload='{"text":":fire: <@'$slack_memberId'> the '$service' is down on '$HOSTNAME' :fire:"}'
    curl -X POST -H 'Content-type: application/json' --data "$payload" $slack_webhook
    tail -n 50 $service_log_file > $service_temp_log_send_file
    sleep 1
    curl -F title='ApplicationLogs' --form-string channels=$slack_channel  -F file=@$service_temp_log_send_file -F filename=$service_temp_log_send_file -F token=$slack_token  $slack_api_url
    crontab -u $service_user -l | grep -v 'service_monitoring.sh'  | crontab -u $service_user -
fi

