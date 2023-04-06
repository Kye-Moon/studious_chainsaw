import boto3
import os
import pytest

from moto import mock_dynamodb


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope='function')
def dynamodb_client(aws_credentials):
    """DynamoDB mock client."""
    with mock_dynamodb():
        client = boto3.client("dynamodb", region_name="ap-southeast-2")
        yield client


@pytest.fixture(scope='function')
def dynamodb_mentions_table(dynamodb_client):
    """Create a DynamoDB surveys table fixture."""
    table = dynamodb_client.create_table(
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
