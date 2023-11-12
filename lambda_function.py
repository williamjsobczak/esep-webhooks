import json
import os
import requests

def lambda_handler(event, context):
    try:
        # Check if the event is an HTTP event with a body
        if 'body' in event:
            # Parse the JSON body
            json_data = json.loads(event['body'])

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
                    print(f'Slack API Response: {response.status_code}')

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
            # If 'body' is not in the event, return an error response
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid event. Missing request body.')
            }
    except Exception as e:
        print(f'Error: {str(e)}')

        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
