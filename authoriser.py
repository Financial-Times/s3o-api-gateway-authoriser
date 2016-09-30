from __future__ import print_function

import urllib2, boto3
from awspolicy import AuthPolicy


def lambda_handler(event, context):

    token = event['authorizationToken']
    principalId = token.split('|')[0]

    tmp = event['methodArn'].split(':')
    apiGatewayArnTmp = tmp[5].split('/')
    awsAccountId = tmp[4]

    restApiId = apiGatewayArnTmp[0]
    stage = apiGatewayArnTmp[1]
    ApiKeyId = restApiId + '-' + stage

    policy = AuthPolicy(principalId, awsAccountId)
    policy.restApiId = restApiId
    policy.region = tmp[3]
    policy.stage = stage

    try:
        if auth_with_s3o(token) or lookupKeyInDynamo(ApiKeyId, token):
            policy.allowAllMethods()
        else:
            policy.denyAllMethods()
    except:
        if lookupKeyInDynamo(ApiKeyId, token):
            policy.allowAllMethods()
        else:
            policy.denyAllMethods()

    return policy.build()


def auth_with_s3o(token):
    s3o_endpoint = "https://s3o.ft.com/token/validate"
    opener = urllib2.build_opener()
    opener.addheaders = [('FT-Authorization', token)]
    return opener.open(s3o_endpoint).getcode() == 204


def lookupKeyInDynamo(ApiKeyId, token):
    client = boto3.resource('dynamodb')
    table = client.Table('lantern_api_gateway_key_store')
    item = table.get_item(Key={'apiId':ApiKeyId}, AttributesToGet=['apiKey'])

    if "Item" in item:
        key = item['Item']['apiKey']
        return token == key
    print ('invalid api key')
    return False