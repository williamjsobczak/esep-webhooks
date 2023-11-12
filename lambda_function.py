import os
import requests
import json

def lambda_handler(event, context):
    try:
        # Log the received event
        print(f'GitHub Event Received: {json.dumps(event)}')

        # Check if the event is an HTTP event
        if isinstance(event, dict):
            # Parse the JSON data
            json_data = event

            # Log the parsed JSON data
            print(f'Parsed JSON Data: {json.dumps(json_data)}')

            # Check if the payload contains information about the created issue
            if 'issue' in json_data and 'html_url' in json_data['issue']:
                # Extract the html_url of the created issue
                issue_html_url = json_data['issue']['html_url']
                print(f'Issue HTML URL: {issue_html_url}')

                # Create the Slack message payload
                payload = {
                    'text': f'Issue Created: {issue_html_url}'
                }
                print(f'Slack Payload: {payload}')

                # Get the Slack URL from the environment variable
                slack_url = os.environ.get('SLACK_URL')

                # Check if the Slack URL is available
                if slack_url:
                    # Send the message to Slack
                    response = requests.post(slack_url, json=payload)
                    print(f'Slack API Response Code: {response.status_code}')
                    print(f'Slack API Response Text: {response.text}')

                    return {
                        'statusCode': response.status_code,
                        'body': json.dumps('Slack message sent successfully!')
                    }
                else:
                    # If the Slack URL is not available, return an error response
                    return {
                        'statusCode': 500,
                        'body': json.dumps('Slack URL is not configured. Please check your environment variables.')
                    }
            else:
                # If the required data is not present in the payload, return an error response
                return {
                    'statusCode': 400,
                    'body': json.dumps('Invalid GitHub Webhook payload. Missing required data.')
                }
        else:
            # If the event is not a dictionary, return an error response
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid event. Expected a dictionary.')
            }
    except Exception as e:
        print(f'Error: {str(e)}')

        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
