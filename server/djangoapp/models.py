from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    # many to one relationship with CarMake model
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    # attributes of a car model
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('WAGON', 'Wagon'),
        ('SUV', 'SUV'),
        ('TRUCK', 'TRUCK'),
        ('VAN', 'Van'),
        ('HATCHBACK', 'Hatchback'),
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(default=2023, validators=[MaxValueValidator(2023), MinValueValidator(2015)])

    def __str__(self):
        return self.name
