from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(dict):
    authenticator = IAMAuthenticator(dict['__OW_API_KEY'])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(dict['__OW_IAM_API_URL'])

    dealer_id = int(dict['dealerId'])

    response = service.post_find(
        db='reviews',
        selector={
            'dealership': {
                '$eq': dealer_id
            }
        }).get_result()

    try:
        result = {
            'statusCode': 200 if len(response['docs']) > 0 else 404,
            'headers': {'Content-Type': 'application/json'},
            'body': {'data': response['docs']}
        }
        return result
    except:
        result = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': {'message': 'Something went wrong'}
        }
        return result
