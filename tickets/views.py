from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view 
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework import status, filters, generics, mixins
from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework import viewsets


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


# Function Based Views 
# 3.1 GET POST 
 
@api_view(['GET', 'POST']) 
def FBV_List(request): 
    
    # GET 
    if request.method == 'GET': 
        guests = Guest.objects.all() 
        serializer = GuestSerializer(guests, many=True) 

        return Response(serializer.data) 

    # POST 
    elif request.method == 'POST': 
        serializer = GuestSerializer(data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 

            return Response(serializer.data, status = status.HTTP_201_CREATED) 
        else: 
            return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST) 


# 3.1 GET PUT DELETE 
@api_view(['GET','PUT', 'DELETE']) 
def FBV_pk(request, pk): 
    
    try: 
        guest = Guest.objects.get(pk=pk) 
    except Guest.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':  
        serializer = GuestSerializer(guest, many=False) 
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
    elif request.method == 'PUT': 
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 
    
    elif request.method =='DELETE': 
        guest.delete() 

        return Response(status=status.HTTP_204_NO_CONTENT)

# CBV 
#4.1 LIST and CREATE (GET - POST) 
class CBV_List(APIView): 
    def get(self, request): 
        guests = Guest.objects.all() 
        serializer = GuestSerializer(guests, many=True) 
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = GuestSerializer(data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        

#4.2 GET PUT DELETE class based views -- pk 
class CBV_pk(APIView): 
    def get_object(self, pk): 
        try: 
            return Guest.objects.get(pk=pk) 
        except Guest.DoesNotExist: 
            raise Http404 

    
    def get(self, request, pk): 
        guest = self.get_object(pk) 
        serializer = GuestSerializer(guest) 
        return Response(serializer.data, status=status.HTTP_200_OK) 

    def put(self, request, pk): 
        guest = self.get_object(pk) 
        serializer = GuestSerializer(instance=guest, data=request.data) 
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
    def delete(self, request, pk): 
        guest = self.get_object(pk) 
        guest.delete() 

        return Response(status=status.HTTP_204_NO_CONTENT) 
    

"""

if your business logic has much work, use function based views 
if you have less business logic, use class based views 

"""


#5 Mixins 
#5.1 Mixins list 
class mixins_list(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    generics.GenericAPIView
): 
    queryset = Guest.objects.all() 
    serializer_class = GuestSerializer 

    def get(self, request): 
        return self.list(request) 

    def post(self, request): 
        return self.create(request)
    


#5.2 mixins get put delete 
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView): 
    queryset = Guest.objects.all() 
    serializer_class = GuestSerializer 

    def get(self, request, pk): 
        return self.retrieve(request)
    
    def put(self, request, pk): 
        return self.update(request) 

    def delete(self, request, pk): 
        return self.destroy(request)  
    


#6.1 Generics get and post 
    
class generics_list(generics.ListCreateAPIView): 
    queryset = Guest.objects.all() 
    serializer_class = GuestSerializer 


#6.2 Generics get, put and delete 
class generics_pk(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Guest.objects.all() 
    serializer_class = GuestSerializer


#7 viewsets 
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all() 
    serializer_class = GuestSerializer 

class viewsets_movie(viewsets.ModelViewSet): 
    queryset = Movie.objects.all() 
    serializer_class = MovieSerializer 

    filter_backends = [filters.SearchFilter]
    search_fields = ['date', 'hall', 'movie']

class viewsets_reservation(viewsets.ModelViewSet): 
    queryset = Reservation.objects.all() 
    serializer_class = ReservationSerializer 


#8 Find Movie 

@api_view(['GET'])
def find_movie(request): 
    movies = Movie.objects.filter(
        movie = request.data['movie'], 
        hall = request.data['hall']
    )
    serializer = MovieSerializer(movies, many=True) 
    
    return Response(serializer.data, status=status.HTTP_200_OK) 


#9 Create New Reservation 
@api_view(['POST'])
def new_reservation(request): 

    movie = Movie.objects.get(movie=request.data['movie'])
    guest = Guest() 

    guest.name = request.data['name']
    guest.mobile = request.data['mobile']

    guest.save()

    reservation = Reservation(
        movie = movie, guest=guest 
    )

    reservation.save() 

    serializer = ReservationSerializer(reservation) 

    return Response(serializer.data, status=status.HTTP_201_CREATED) 

    