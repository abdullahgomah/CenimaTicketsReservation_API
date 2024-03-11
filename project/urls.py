from django.contrib import admin
from django.urls import path

from tickets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    

    #1 
    path('django/jsonresponsenomodel/', views.no_rest_no_model),

    #2 
    path('django/jsonresponsewithmodel/', views.no_rest_from_model),  
]
