# PongiBot

A WIP chinese chatbot on Facebook Messenger.

The bot is using tuling123 api for response now.
Code are deployed with AWS Lambda & API gateway.

To setup the bot:

1. setup venv and requirement 
```
cd pongibot
virtualenv venv_bot
source venv_bot/bin/activate
pip install -r requirements.txt
```

2. generate aws lambda zip
```
cd pongibot
. create_aws_lambda_zip.sh
```

3. upload pongibot_v0.0.1.zip to aws lambda
```
