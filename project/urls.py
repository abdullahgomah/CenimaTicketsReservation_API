from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter 

router = DefaultRouter() 
router.register('guests', views.viewsets_guest)
router.register('movies', views.viewsets_movie)
router.register('reservations', views.viewsets_reservation)



urlpatterns = [
    path('admin/', admin.site.urls),
    

    #1 
    path('django/jsonresponsenomodel/', views.no_rest_no_model),

    #2 
    path('django/jsonresponsewithmodel/', views.no_rest_from_model),  
    
    #3 
    path('rest/fbvlist/', views.FBV_List),

    #4
    path('rest/fbvlist/<int:pk>/', views.FBV_pk),

    #5 Class Based Views, Api View 
    path('rest/cbv/', views.CBV_List.as_view()),

    #6 
    path('rest/cbv/<int:pk>/', views.CBV_pk.as_view()),


    #7 
    path('rest/mixins/', views.mixins_list.as_view()), 
    path('rest/mixins/<int:pk>/', views.mixins_pk.as_view()),

    #8 
    path('rest/generic/', views.generics_list.as_view()), 
    path('rest/generic/<int:pk>/', views.generics_pk.as_view()),

    #9 
    path('rest/viewsets/', include(router.urls)) , 

    #10 
    path('rest/fbv/findmovie/', views.find_movie), 

    #11 
    path('rest/fbv/newreservation/', views.new_reservation), 
]
