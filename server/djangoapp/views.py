from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .restapis import get_dealers_from_cf
from .restapis import get_dealer_reviews_from_cf
from .restapis import post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://ed9eb290.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealership_by_id(request, **kwargs):
    if request.method == "GET":
        url = "https://ed9eb290.us-south.apigw.appdomain.cloud/api/dealership"
        state = kwargs.get('state')
        dealer_id = kwargs.get('dealerId')
        print(kwargs)
        print("GET from {}".format(url))
        dealership = []
        if dealer_id:
            dealership = get_dealers_from_cf(url, dealerId=dealer_id)
        if state:
            dealership = get_dealers_from_cf(url, state=state)
        if dealer_id and state:
            dealership = get_dealers_from_cf(url, dealerId=dealer_id, state=state)
        return HttpResponse(dealership)


def get_dealer_details(request, dealerId):
    context = {}
    if request.method == 'GET':
        url = "https://ed9eb290.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealerId)
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealerId):
    payload = {'review': {}}
    payload['review']["dealership"] = dealerId
    payload['review']["name"] = "Ron Swanson"
    payload['review']["purchase"] = True
    payload["review"]['review'] = "Acceptable"
    payload["purchase_date"] = datetime.utcnow().isoformat()
    payload['review']["car_make"] = "Alfa-Romeo"
    payload['review']["car_model"] = "Stelvio"
    payload['review']["car_year"] = 2022
    payload['review']["id"] = 2023
    print("==> PAYLOAD = {}".format(payload))
    print("REQUEST ==> {}".format(request))
    if request.method == 'POST':
        url = "https://ed9eb290.us-south.apigw.appdomain.cloud/api/review/post"
        print("==> URL -> {}".format(url))
        response = post_request(url, payload, dealerId=dealerId)
        print("==> RESPONSE = {}".format(response.text))
        return HttpResponse(response.text)
    elif request.method == 'GET':
        context = {}
        render(request, 'djangoapp/add_review.html', context)
