const DynamoDbAdapter = require('../../_helpers/adapters/DynamoDbAdapter')

describe('DynamoDB Adapter', () => {
  it('should query by field', async () => {
    // GIVEN
    const db = new DynamoDbAdapter()

    // WHEN
    const results = await db.queryByField(process.env.TABLE_NAME, 'id', 'fake-fake-fake')

    // THEN
    expect(results).toBeTruthy()
    expect(results.Count).toBe(0)
  })

  it('should create & delete item', async () => {
    // GIVEN
    const db = new DynamoDbAdapter()
    const paramsCreate = {
      Item: {
        id: { S: 'SampleId' },
        Type: { S: 'SampleId' },
      },
      ReturnConsumedCapacity: 'TOTAL',
      TableName: process.env.TABLE_NAME
    }
    const paramsDelete = {
      Key: {
         id: { S: 'SampleId' },
      },
      ReturnConsumedCapacity: 'TOTAL',
      TableName: process.env.TABLE_NAME
    }

    // WHEN
    const createResults = await db.create(paramsCreate)
    const deleteResults = await db.delete(paramsDelete)
    const check = await db.queryByField(process.env.TABLE_NAME, 'id', 'SampleId')

    // THEN
    expect(createResults).toBeTruthy()
    expect(createResults.ConsumedCapacity.TableName).toMatch(process.env.TABLE_NAME)
    expect(createResults.ConsumedCapacity.CapacityUnits).toBe(1)
    expect(deleteResults.ConsumedCapacity.TableName).toMatch(process.env.TABLE_NAME)
    expect(deleteResults.ConsumedCapacity.CapacityUnits).toBe(1)
    expect(check.Count).toBe(0)
  })

  it('should get item', async () => {
    // GIVEN
    const db = new DynamoDbAdapter()
    const paramsCreate = {
      Item: {
         id: { S: 'SampleId' },
        Type: { S: 'TestEntity' },
      },
      ReturnConsumedCapacity: 'TOTAL',
      TableName: process.env.TABLE_NAME
    }
    const paramsDelete = {
      Key: {
         id: { S: 'SampleId' }
      },
      ReturnConsumedCapacity: 'TOTAL',
      TableName: process.env.TABLE_NAME
    }
    const paramsGet = {
      Key: {
         id: { S: 'SampleId' }
      },
      ReturnConsumedCapacity: 'TOTAL',
      TableName: process.env.TABLE_NAME
    }

    // WHEN
    const createResults = await db.create(paramsCreate)
    const getResults = await db.get(paramsGet)
    const deleteResults = await db.delete(paramsDelete)
    const check = await db.queryByField(process.env.TABLE_NAME, 'id', 'SampleId')

    // THEN
    expect(createResults).toBeTruthy()
    expect(createResults.ConsumedCapacity.TableName).toMatch(process.env.TABLE_NAME)
    expect(createResults.ConsumedCapacity.CapacityUnits).toBe(1)
    expect(getResults.Item.id.S).toBe('SampleId')
    expect(getResults.Item.Type.S).toBe('TestEntity')
    expect(deleteResults.ConsumedCapacity.TableName).toMatch(process.env.TABLE_NAME)
    expect(deleteResults.ConsumedCapacity.CapacityUnits).toBe(1)
    expect(check.Count).toBe(0)
  })
})
