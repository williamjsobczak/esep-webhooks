import json
import os
import requests

def lambda_handler(event, context):
    json_data = json.loads(event['body'])

    if 'issue' in json_data and 'html_url' in json_data['issue']:
        # Extract the html_url of the created issue
        issue_html_url = json_data['issue']['html_url']

        # Create the Slack message payload
        payload = {
            'text': f'Issue Created: {issue_html_url}'
        }

        # Get the Slack URL from the environment variable
        slack_url = os.environ.get('SLACK_URL')

        # Check if the Slack URL is available
        if slack_url:
            # Post message to Slack channel
            response = requests.post(slack_url, json=payload)

            # Log the response status code
            print(f'Slack API Response: {response.status_code}')

            return {
                'statusCode': response.status_code,
                'body': json.dumps('Slack message sent successfully!')
            }
        else:
            # Returns an error response if the Slack URL is not available
            return {
                'statusCode': 500,
                'body': json.dumps('Slack URL is not configured. Please check your environment variables.')
            }
    else:
        # Returns an error response if the required data is not present in the payload
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid GitHub Webhook payload. Missing required data.')
        }