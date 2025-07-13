from dotenv import load_dotenv

load_dotenv()

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from pathlib import Path
def initialize(credentials_fp:Path):
    global SCOPES, SERVICE

    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    flow = InstalledAppFlow.from_client_secrets_file(credentials_fp, SCOPES)
    creds = flow.run_local_server(port=0)

    SERVICE = build("gmail", "v1", credentials=creds)


def send_html_email(recipient, subject, html_content):
    user_id = "me"

    msg = MIMEText(html_content, "html")
    msg["Subject"] = subject
    msg["To"] = recipient

    create_message = {
        "raw": base64.urlsafe_b64encode(bytes(msg.as_string(), "utf-8")).decode(
            "utf-8"
        ),
        "payload": {"mimeType": "text/html"},
    }

    try:
        message = (
            SERVICE.users()
            .messages()
            .send(userId=user_id, body=create_message)
            .execute()
        )
        print(f'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(f"An error occurred: {error}")
        message = None


if __name__ == "__main__":
    pass
