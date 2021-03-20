import json
import boto3
import decimal
import os


ERROR_SUMMARY_TABLE = os.environ['ERROR_SUMMARY_TABLE']
ERROR_DETAIL_TABLE = os.environ['ERROR_DETAIL_TABLE']


def json_encode_decimal(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")


def get_error_summary(event, context):
    if event['httpMethod']=='GET' and '/fixr/data/error/summary' in event['path']:

        table = boto3.resource('dynamodb').Table(ERROR_SUMMARY_TABLE)
        results = table.scan()['Items']
        return {
        'statusCode': 200,
        'body': json.dumps(results,default=json_encode_decimal)
        }

def get_error_details_summary(event, context):
    if event['httpMethod']=='GET' and '/fixr/data/error/details/summary' in event['path']:

        table = boto3.resource('dynamodb').Table(ERROR_DETAIL_TABLE)
        results = table.scan()['Items']
        return {
        'statusCode': 200,
        'body': json.dumps(results,default=json_encode_decimal)
        }    
    

def get_error_detail(event, context):
    if event['httpMethod']=='GET' and '/fixr/data/error/details' in event['path']:

        errorId = int(event['path'].rsplit('/', 1)[-1])
        table = boto3.resource('dynamodb').Table(ERROR_DETAIL_TABLE)
        resp = table.get_item(
        Key={
            'ERROR_ID': errorId 
        }
        )
        item = resp['Item']
        if not item:
            return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Error does not exist'})
        }
        else:
            return {
            'statusCode': 200,
            'body': json.dumps(item,default=json_encode_decimal)
            }

def update_one_error(event, context):
    if event['httpMethod']=='PATCH' and '/fixr/data/error/details' in event['path']:

        errorId = int(event['path'].rsplit('/', 1)[-1])
        body = event['body']
        table = boto3.resource('dynamodb').Table(ERROR_DETAIL_TABLE)
        response = table.update_item(
        Key={'ERROR_ID': errorId },
        UpdateExpression="set PAYLOAD = :a",
        ExpressionAttributeValues={
            ':a': body
        },
        ReturnValues="UPDATED_NEW"
        )

        return {
        'statusCode': 200,
        'body': json.dumps({'message': response})
        }        
