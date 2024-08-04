# README

## Overview

This Python script is designed to automate responses to customer messages in Intercom based on the current time (work hours or off-hours). It checks the current time, sends an appropriate message, and can snooze conversations during off-hours. The script uses the Intercom API for sending messages and managing conversations.

## Features

- **Automatic Detection of Work Hours:** The script checks if the current time falls within predefined work hours.
- **Automated Responses:** Sends predefined messages during work hours and off-hours.
- **Snoozing Conversations:** Automatically snoozes conversations until the next workday if they are received outside of work hours.
- **Alert Messages:** Sends additional alert messages regarding specific issues.

## Requirements

- AWS Lambda with Python 3.11.x runtime
- Required Python packages: `os`, `json`, `requests`, `datetime`, `pytz`
- Environment variables:
  - `INTERCOM_ACCESS_TOKEN`: Your Intercom API access token.
  - `ADMIN_URL`: URL to fetch the admin ID from Intercom.

## Installation

1. **Clone the Repository or Download the Script:**
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install the Required Python Packages:**
    ```sh
    pip install requests pytz
    ```

3. **Set the Required Environment Variables:**
    ```sh
    export INTERCOM_ACCESS_TOKEN=your_intercom_access_token
    export ADMIN_URL=your_admin_url
    ```

## Configuration

- **Work Hours:** The default work hours are set from 8:00 AM to 5:00 PM WAT (Africa/Lagos timezone). You can adjust these settings in the script if needed.
  ```python
  WORK_HOURS_START = time(8, 0)
  WORK_HOURS_END = time(17, 0)
  TIMEZONE = pytz.timezone('Africa/Lagos')  # Adjust the timezone as needed
  ```

## Usage

### AWS Lambda Deployment

1. **Create a Lambda Function:**
    - Go to the AWS Lambda console.
    - Create a new function with the Python 3.11.x runtime.

2. **Set Environment Variables:**
    - Add `INTERCOM_ACCESS_TOKEN` and `ADMIN_URL` as environment variables in your Lambda function configuration.

3. **Deploy the Script:**
    - Package the script and its dependencies using a tool like `zip` or `AWS SAM`.
    - Upload the deployment package to your Lambda function.

4. **Configure Intercom to Send Events to Your Lambda Function:**
    - Set up a webhook in Intercom to trigger your Lambda function on specific events (e.g., conversation creation).

## Functions

### `is_work_hours()`
Checks if the current time is within predefined work hours.

### `admin_id()`
Fetches the admin ID from Intercom using the provided `ADMIN_URL`.

### `send_message_during_office_hours(conversation_id, admin_id, user_name=None)`
Sends a message during work hours.

### `send_out_of_office_message(conversation_id, admin_id, user_name=None)`
Sends a message during off-hours.

### `send_alert_message(conversation_id, admin_id, user_name=None)`
Sends an alert message regarding specific issues.

### `snooze_conversation(conversation_id, admin_id)`
Snoozes the conversation until the next workday.

### `lambda_handler(event, context)`
Handles incoming events from Intercom, sending appropriate messages based on the time of the day.

## Example

Here’s an example of how to use the script in AWS Lambda:

1. **Set up the Lambda function with the required environment variables.**
2. **Deploy the script to AWS Lambda.**
3. **Configure Intercom to send events to your Lambda function.**

## Troubleshooting

1. **Ensure Environment Variables are Set:** Verify that `INTERCOM_ACCESS_TOKEN` and `ADMIN_URL` are correctly set in your environment.
2. **Check Dependencies:** Make sure all required Python packages are installed.
3. **Review Logs:** Check the logs for any errors related to API requests or missing data.

For further assistance, refer to the Intercom API documentation or reach out to support.
