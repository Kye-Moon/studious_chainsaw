import os

import boto3

# Let's use Amazon S3
client = boto3.client('sns')

class TestClass:
    def test_snsmessage_triggers_lambda(self):
        response = client.list_subscriptions_by_topic(
            TopicArn=os.environ["INTEGRATION_REQUEST_TOPIC_ARN"]
        )
        print(response)


