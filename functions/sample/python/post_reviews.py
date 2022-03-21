from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator(dict['__OW_API_KEY'])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(dict['__OW_IAM_API_URL'])

    response = service.post_document(db='reviews', document=dict["review"]).get_result()

    try:
        result = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': {'data': response}
        }
        return result
    except:
        return {
            'statusCode': 404,
            'message': 'Something went wrong'
        }
