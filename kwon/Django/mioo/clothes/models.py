from django.db import models

# Create your models here.
from django.db import models

class clothes(models.Model):
    kind = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    size = models.CharField(max_length=30)

    def __str__(self) :
        return self.name



'''

class Clothes():
    def __init__(self,name,price):
        self.name = name
        self.price = price
        
class Pants(Clothes):
    def __init__(self,name,price,size):
        super().__init__(name,price)
        self.size = size

        
class Top(Clothes):
    def __init__(self,name,price,size):
        super().__init__(name,price)
        self.size = size

'''
