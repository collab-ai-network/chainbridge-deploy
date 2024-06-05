import os
import subprocess
import requests
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configuration variables
service_user = "ubuntu"
service = "Chainbridge"
slack_webhook = "https://hooks.slack.com/services/xxxxxxxxxxxxx"
slack_token = "xoxb-xxxxxxxxxxxxxxxxx"
slack_memberId = "xxxxxxxxxx"
slack_channel = "xxxxxxxxxx"
service_log_file = "./chainbridge.log"
service_temp_log_send_file = "sendFile.txt"

def is_service_running(service_name):
    """Check if the service is running"""
    try:
        output = subprocess.check_output(["pgrep", "-x", service_name])
        return bool(output.strip())
    except subprocess.CalledProcessError:
        return False

def send_slack_notification(message):
    """Send a notification to Slack"""
    payload = {"text": f":fire: <@{slack_memberId}> the {service} is down on {os.uname().nodename} :fire:"}
    response = requests.post(slack_webhook, json=payload)
    return response.status_code == 200

def upload_file_to_slack(file_path, slack_channel, slack_token):
    """Upload a file to Slack"""
    client = WebClient(token=slack_token)
    try:
        response = client.files_upload_v2(
            channel=slack_channel,
            title="Log file",
            file=file_path,
            initial_comment="Here is the Log file:",
        )
        return response.get("ok", False)
    except SlackApiError as e:
        print(f"Error uploading file to Slack: {e.response['error']}")
        return False

# Main script logic
if is_service_running(service):
    print(f"{service} service running")
else:
    print("service not running")
    # Send Slack notification
    if send_slack_notification(f"The {service} is down on {os.uname().nodename}"):
        print("Slack notification sent successfully.")
    else:
        print("Failed to send Slack notification.")

    # Create temporary log file
    with open(service_log_file, 'r') as log_file:
        log_lines = log_file.readlines()[-50:]
    with open(service_temp_log_send_file, 'w') as temp_log_file:
        temp_log_file.writelines(log_lines)

    time.sleep(1)

    # Upload log file to Slack
    if upload_file_to_slack(service_temp_log_send_file, slack_channel, slack_token):
        print("Log file uploaded to Slack successfully.")
    else:
        print("Failed to upload log file to Slack.")