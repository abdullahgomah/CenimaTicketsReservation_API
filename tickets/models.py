from django.db import models

# Guest -- Movie -- Reservation 

class Movie(models.Model):

    hall = models.CharField(max_length=10) 
    movie = models.CharField(max_length=10) 
    date = models.DateField()
    

    class Meta:
        verbose_name = ("Movie")
        verbose_name_plural = ("Movies")

    def __str__(self): 
        return self.movie 

  

class Guest(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=30)

    class Meta:
        verbose_name = ("Guest")
        verbose_name_plural = ("Guests")

    def __str__(self):
        return self.name

class Reservation(models.Model):

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservation')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reservation')
    
    class Meta:
        verbose_name = ("Reservation")
        verbose_name_plural = ("Reservations")

    def __str__(self):
        return str(self.guest.name)
