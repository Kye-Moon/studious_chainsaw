import json

from aws_lambda_powertools.utilities.data_classes import (
    event_source,
    SQSEvent,
)

from src.dynamodb import DynamoDB
from src.service_modules.product_hunt_post_service import process_ph_post_integration_record


@event_source(data_class=SQSEvent)
def handler(event: SQSEvent, context):
    db = DynamoDB(table_name="mentions", instance="prod")
    print("product hunt integration handler function has been invoked")
    try:
        for record in event.records:  # batch size is set to 1, but can make this a batch if needed
            record_message = json.loads(record.body)
            campaign_id = record_message["campaignId"]
            url = record_message["requestUrl"]
            process_ph_post_integration_record(url=url, campaign_id=campaign_id, db=db)
    except Exception as e:
        print(e)
