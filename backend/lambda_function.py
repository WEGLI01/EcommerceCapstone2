import json
import boto3
import uuid
import logging
import urllib.parse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        if 'body' not in event or event['body'] is None:
            raise ValueError("Request body is missing or null")
        
        raw_body = event['body']
        logger.info(f"Raw body: {raw_body}")
        
        content_type = event.get('headers', {}).get('Content-Type', '')
        logger.info(f"Content-Type: {content_type}")
        
        if 'application/x-www-form-urlencoded' in content_type:
            parsed_body = urllib.parse.parse_qs(raw_body)
            json_string = parsed_body.get('data', [''])[0]
            if not json_string:
                raise ValueError("Missing 'data' field in form submission")
            body = json.loads(json_string)
            logger.info(f"Parsed form data (JSON): {body}")
        else:
            body = json.loads(raw_body)
            logger.info(f"Parsed JSON body: {body}")
        
        order_id = str(uuid.uuid4())
        table.put_item(Item={
            'OrderID': order_id,
            'CustomerID': body['customerId'],
            'Item': body['item'],
            'DeliverySlot': body['deliverySlot'],
            'DeliveryInstructions': body['instructions']
        })
        return {
            'statusCode': 301,
            'headers': {
                'Location': 'http://wesley-ecommerce-capstone.s3-website.us-east-2.amazonaws.com/confirmation.html',
                'Access-Control-Allow-Origin': 'http://wesley-ecommerce-capstone.s3-website.us-east-2.amazonaws.com',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': 'http://wesley-ecommerce-capstone.s3-website.us-east-2.amazonaws.com',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({'error': str(e)})
        }