from django.db import models
from django.utils.timezone import now
import uuid


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    id = models.AutoField(
        primary_key=True,
        unique=True
    )
    name = models.CharField(
        null=False,
        max_length=20
    )
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name + "," + \
               self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), null=False)
    car_make = models.ForeignKey(CarMake, null=False)
    year = models.DateField(default=now, null=False)

    # List of choices for Type field
    SUV = 'suv'
    VAN = 'van'
    WAGON = 'wagon'
    COUPE = 'coupe'
    TRUCK = 'truck'
    SEDAN = 'sedan'
    TYPE_CHOICES = [
        (SUV, 'Suv'),
        (VAN, 'Van'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe'),
        (TRUCK, 'Truck'),
        (SEDAN, 'Sedan')
    ]

    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )

    def __str__(self):
        return self.id + "," +\
               self.car_make + "," +\
               self.type + "," +\
               self.year

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
