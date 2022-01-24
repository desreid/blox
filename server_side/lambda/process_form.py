import os
import json
import urllib.parse
import boto3
import base64
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

        
def lambda_handler(event, context):
    user_data = extract_user_data(event)
    if validate_user_data(user_data):
        status = save_data(user_data)
        if status:
            return send_redirect_response()
        else:
            return send_json_response(500, "Database error")
    else:
        return send_json_response(400, "Invalid user data")

def extract_user_data(event):
    """
    Utility to extract the form data from the AWS lambda event
    returns data as a python dict
    """
    LOGGER.info("Extracting User Data from HTML form")
    LOGGER.debug(event)
    LOGGER.debug("Base 64 encoded form data is: %s", event['body'])
    form_bytes = event.get('body').encode()
    decoded_form = base64.b64decode(form_bytes)
    decoded_form_string = decoded_form.decode()
    LOGGER.debug("decoded form data is " + decoded_form_string)
    form_data_as_dict = urllib.parse.parse_qs(decoded_form_string)
    LOGGER.info("User data is %s", json.dumps(form_data_as_dict))
    return form_data_as_dict
    
def validate_user_data(user_data):
    """
    Validates the information sent by the user
    Returns true or false
    """
    # TO_DO
    return True
    
def send_json_response(status, error=None):
    """
    Creates the response to return to client
    """
    body = {
        "aws_region":  os.environ['AWS_REGION']
    }
    if error is not None:
        body['error'] = error
    response = {
            "statusCode":str(status),
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(body)
    }
    return response
    
def send_redirect_response():
    """
    Success, redirects user to thank you page
    """
    # TODO make the redirect page configurable
    thankyou_page = 'http://earthblox.s3-website-eu-west-1.amazonaws.com/thanks.html'
    response = {
            "statusCode":301,
            "headers": {
                "Location": thankyou_page
            },
    }
    return response
    
def save_data(user_data):
    """
    save the data to dynamo db
    returns true on success
    """
    LOGGER.info("Processing user datas %s", user_data)
    table_name = 'contacts'
    
    item = {
        # TODO exception handling for requests that dont contain the right fields. EG user_data.get('email')[0] will throw an exception if email doesn't exist
        'email': user_data.get('email')[0],
        'company': user_data.get('company')[0],
        'consent': user_data.get('consent')[0],
        'confirmed_certification': user_data.get('confirmed_certification')[0],
        'data_types': user_data.get('data_types'), # store as list
        'countries': user_data.get('countries') # store as list
    }
    LOGGER.info("Saving item to DB %s", item)
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        LOGGER.debug("Using table %s created on %s", table_name, table.creation_date_time)
        table.put_item(Item=item)
    except Exception as e:
        LOGGER.error("Database error occurred %s", e)
        return False
    return True