from contextlib import contextmanager


class TestDynamoDBMentions:
    """Test CRUD operations on mock DynamoDB table"""

    TABLE_NAME = "mentions"

    def test_create_table(self, dynamodb_client):
        """Test creation of 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):
            res = dynamodb_client.describe_table(TableName=self.TABLE_NAME)
            res2 = dynamodb_client.list_tables()

            assert res['Table']['TableName'] == self.TABLE_NAME
            assert res2['TableNames'] == [self.TABLE_NAME]

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
            assert res['Item']['PK'] == {"S": "attribute1_value"}
            assert len(res['Item']) == 2


@contextmanager
def create_table(dynamodb_client):
    """Create mock DynamoDB table to test full CRUD operations"""

    dynamodb_client.create_table(
        TableName="mentions",
        KeySchema=[
            {
                'AttributeName': 'PK',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'SK',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PK',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'SK',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    yield
