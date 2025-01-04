# TalentScout Hiring Assistant Chatbot

## Overview

The TalentScout Hiring Assistant is a Streamlit-based web application designed to assist in the hiring process by generating technical interview questions and evaluating candidates' answers. It leverages Google’s generative AI model to create tailored questions based on the candidate's specified tech stack.

## Features

- Generate technical interview questions based on a candidate's skills.
- Evaluate candidates' answers and provide scores.
- Collect candidate information such as name, email, phone number, experience, desired position, and tech stack.
- Save candidate data for further analysis.

## Requirements

To run this application, you need to have Python installed along with the following packages:

- `streamlit`
- `google-generativeai`

You can install these packages using pip:

```
pip install -r requirements.txt
```

## Usage

1. Clone this repository or download the files.
2. Navigate to the project directory.
3. **For Local Development:** You can hardcode your API key directly in the code (as shown in `app.py` comments).
4. **For AWS Deployment:** Use AWS Secrets Manager to manage your API key securely. Replace the hardcoded API key in your code with a function that retrieves it from Secrets Manager.
5. Run the application using Streamlit:

```
streamlit run app.py
```

6. Open your web browser and go to `http://localhost:8501` to access the application.

## Managing Secrets on AWS

If you want to run this application on AWS, it is recommended to manage your API key securely using AWS Secrets Manager:

1. **Store the API Key:**
   - Go to the AWS Management Console.
   - Navigate to **Secrets Manager** and create a new secret with your API key.

2. **Update Your Application Code:**
   Replace the hardcoded API key in your code with a function that retrieves it from AWS Secrets Manager. Here’s an example of how you can do this:

```
import boto3
import json

def get_api_key():
    secret_name = "TalentScoutAPIKey"
    region_name = "your-region"  # e.g., "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret)
        return secret_dict['API_KEY']
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None

# Use the retrieved API key in your application
API_KEY = get_api_key()
```

### Notes:
- Ensure that your AWS IAM role has permissions to access Secrets Manager and retrieve secrets.
- Replace `"your-region"` with the appropriate AWS region where you stored your secret.

## Developer Information

- **Name:** Kshitiz Singhal
- **Contact:** kshitiz1303@gmail.com
- **LinkedIn:** [Kshitiz LinkedIn](https://www.linkedin.com/in/kshitiz-singhal-35a92a32a/)
- **GitHub:** [Kshitiz GitHub](https://github.com/kshitizsinghal13)
