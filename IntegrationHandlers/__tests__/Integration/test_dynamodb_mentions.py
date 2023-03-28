import pytest
from .test_dynamodb import create_table


def test_put_item(self, dynamodb_client):
    """Test adding an item to 'my-test-table' DynamoDB table"""

    with create_table(dynamodb_client):
        add_item = dynamodb_client.put_item(
            TableName=self.TABLE_NAME,
            Item={
                "PK": {"S": "attribute1_value"},
                "SK": {"S": "attribute2_value"},
            },
        )

        res = dynamodb_client.get_item(
            TableName=self.TABLE_NAME,
            Key={
                "PK": {"S": "attribute1_value"},
                "SK": {"S": "attribute2_value"},
            },
        )

        assert add_item['ResponseMetadata']['HTTPStatusCode'] == 200
        assert res['Item']['attribute1'] == {"S": "attribute1_value"}
        assert len(res['Item']) == 2
