import json
import logging

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework.decorators import api_view

from .models import CarModel
from .restapis import get_dealer_reviews_from_cf
from .restapis import get_dealers_from_cf
from .restapis import post_request
from .restapis import analyze_review_sentiments

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
        context["dealerId"] = dealerId
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# @api_view(['GET', 'POST'])
def add_review(request, dealerId):
    context = {
        "dealerId": dealerId
    }
    get_url = url = "https://ed9eb290.us-south.apigw.appdomain.cloud/api/dealership"
    car_dealer = get_dealers_from_cf(get_url, dealerId=dealerId)
    if request.method == 'POST':
        post_url = "https://ed9eb290.us-south.apigw.appdomain.cloud/api/review"
        form_data = request.POST
        car = CarModel.objects.get(id=form_data.get('car'))
        payload = {
            "review": {
                'id': 2022,
                'review': form_data.get('review'),
                'car_make': car.car_make.name,
                'car_year': int(car.year.strftime("%Y")),
                'car_model': car.name,
                'purchase': True if form_data.get('purchase') == 'on' else False,
                'purchase_date': form_data.get('purchase_date'),
                'name': request.user.get_full_name(),
                'dealership': dealerId,
                'sentiment': analyze_review_sentiments(form_data.get('review'))
            }
        }
        response = post_request(post_url, payload)
        print("With url {}, \nresponse => {}".format(post_url, response))
        return redirect('djangoapp:dealer_details', dealerId=dealerId)
    elif request.method == 'GET':
        context['cars'] = CarModel.objects.all()
        context['dealership'] = car_dealer[0]
        return render(request, 'djangoapp/add_review.html', context)
