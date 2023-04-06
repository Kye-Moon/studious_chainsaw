import json

from aws_lambda_powertools.utilities.data_classes import event_source, SQSEvent
from .clients.dynamodb import DynamoDB
from .services.scrape_producthunt_reviews import process_producthunt_review_integration

@event_source(data_class=SQSEvent)
def handler(event:SQSEvent, context):
    """
    This function is the entry point for the product hunt review integration lambda function.
    """
    db = DynamoDB(table_name="mentions", instance="prod")
    print("product hunt review integration handler function has been invoked")
    try:
        for record in event.records:  # batch size is set to 1, but can make this a batch if needed
            record_message = json.loads(record.body)
            campaign_id = record_message["campaignId"]
            requestUrl = record_message["requestUrl"]
            product_slug = requestUrl.split("/")[-2]
            process_producthunt_review_integration(campaign_id=campaign_id, product_slug=product_slug, db=db)
    except Exception as e:
        print(e)
