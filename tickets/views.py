from django.shortcuts import render
from django.http import JsonResponse
from .models import Guest, Movie, Reservation

#1 without REST framework and no model query 
def no_rest_no_model(request): 
    guests = [
        {
            'id': 1,
            'name': "Omar", 
            'mobile': "01508420041"
        }, 
        {
            "id": 2, 
            "name": "Abdullah", 
            "mobile": "01058432244"
        }
    ]

    return JsonResponse(guests, safe=False)   


#2 without REST, with model 
def no_rest_from_model(request):
    data = Guest.objects.all() # I wanna this end point 

    response = {
        'guests': list(data.values("name", "mobile"))
    }

    return JsonResponse(response, safe=False) 


# GET -- POST 
# pk query = GET 
# PUT = update 
# DELETE = delete 


