from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt

# week 3: import models
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request):
    '''Create a `logout_request` view to handle sign out request
    '''
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    # initialise empty context
    # context = {}

    # create a json data object containing body of request
    data = json.loads(request.body)

    # get raw data from data object
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    # check if username and email already exists
    # email_exist = False

    # Check if user already exists
    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except Exception as err:
        # If not, simply log this as a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user, create the user
    if not username_exist:

        # Create user in auth_user table
        user = User.objects.create_user(
            username=username, 
            first_name=first_name, 
            last_name=last_name, 
            password=password, 
            email=email
        )

        # Login the user and redirect to list page
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}

    # if not new user, raise a suitable error
    else:
        data = {"userName": username, "error": "Already Registered"}

    # return the json response
    return JsonResponse(data)


def get_cars(request):
    """get list of cars
    """
    count = CarMake.objects.filter().count()
    print(count)
    if (count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name, 
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    '''Render list of dealerships.
    All by default, particular state if state is passed.
    '''
    if (state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    '''Render the dealer details.
    '''
    if (dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    '''Render the reviews of a dealer.
    '''
    if (dealer_id):
        # get the relevant endpoint corresponding to reviews for the dealer
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `add_review` view to submit a review
def add_review(request):
    '''View to submit a review.
    '''
    # first, check if user is authenticated before allowing to post review
    if (request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            # call method to post a review
            response = post_review(data)

            # return success status and message as JSON
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
