from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.TimeField()
    date = models.DateField()
    seats_available = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"<Movie: {self.name} :{self.date} {self.time}>"


class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    customer_email = models.EmailField()
