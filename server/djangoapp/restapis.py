import requests
import json
from .models import CarDealer
from .models import DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# base_url = 'https://ed9eb290.us-south.apigw.appdomain.cloud/api'
#             https://ed9eb290.us-south.apigw.appdomain.cloud/api
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                'X-IBM-Client-Id': '2cc65619-64e8-411d-bb5b-bd37981d047e'
            },
            params=kwargs
        )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("==> JSON PAYLOAD -> {}".format(json.dumps(json_payload)))
    try:
        response = requests.post(
            url,
            headers={
                'Content-Type': 'application/json',
                'X-IBM-Client-Id': '2cc65619-64e8-411d-bb5b-bd37981d047e'
            },
            # json=json.dumps(json_payload),
            data=json_payload,
            params=kwargs
        )
        print(response)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = None
    if len(kwargs):
        dealer_id = kwargs.get('dealerId')
        state = kwargs.get('state')
        if dealer_id:
            json_result = get_request(url, dealerId=dealer_id)
        if state:
            json_result = get_request(url, state=state)
        if (dealer_id and state):
            json_result = get_request(url, state=state, dealerId=dealer_id)
        dealers = json_result["body"]
        for d in dealers:
            dealer = CarDealer(
                address=d["address"],
                city=d["city"],
                full_name=d["full_name"],
                id=d["id"],
                lat=d["lat"],
                long=d["long"],
                short_name=d["short_name"],
                st=d["st"],
                zip=d["zip"]
            )
            results.append(dealer)
        return results
    else:
        json_result = get_request(url)
    if json_result:
        dealers = json_result["body"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["body"]["data"]
        for review in reviews:
            review_doc = review
            review_obj = DealerReview(
                dealership=review_doc['dealership'],
                name=review_doc['name'],
                purchase=review_doc['purchase'],
                review=review_doc['review'],
                purchase_date=review_doc['purchase_date'],
                car_make=review_doc['car_make'],
                car_model=review_doc['car_model'],
                car_year=review_doc['car_year'],
                # sentiment=review_doc['sentiment'],
                id=review_doc['id']
            )
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    # - Call get_request() with specified arguments
    # - Get the returned sentiment label such as Positive or Negative
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/20cd0fce-c34c-44e6-8a7d-25e2cc753f61'
    apikey = 't-NobZ1HFFoyOzrUHTF2pfJg16ee0KnoEMaVHuPjTeTj'
    authenticator = IAMAuthenticator(apikey)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            sentiment=SentimentOptions(targets=[text])
        )
    ).get_result()
    label = json.dumps(response, indent=2)
    return (label)
