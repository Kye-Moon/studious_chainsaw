import boto3


class DynamoDB:
    def __init__(self, table_name: str, instance: str = "test"):
        self.instance = f"{instance}"
        if self.instance == "dev" or self.instance == "prod":
            self.table_name = f"{table_name}"
        else:
            self.table_name = f"{table_name}-{self.instance}"
        self.dynamodb_client = boto3.client('dynamodb', region_name="ap-southeast-2")
        self.dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-2")
        self.table = self.dynamodb.Table(self.table_name)

    def get_item(self, pk: str, sk: str):
        return self.table.get_item(Key={"PK": pk, "SK": sk})

    def get_items(self, pk: str):
        return self.table.query(KeyConditionExpression="PK = :pk", ExpressionAttributeValues={":pk": pk})

    def put_item(self, pk: str, sk: str, **kwargs):
        return self.table.put_item(Item={"PK": pk, "SK": sk, **kwargs})

    def get_table(self):
        tables = self.dynamodb_client.list_tables()
        if self.table_name in tables['TableNames']:
            return
        else:
            self.create_table()
            self.table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)

    def delete_table(self):
        return self.dynamodb_client.delete_table(TableName=self.table_name)


    def create_table(self):
        return self.dynamodb_client.create_table(
            TableName=self.table_name,
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
            BillingMode='PAY_PER_REQUEST',
        )
