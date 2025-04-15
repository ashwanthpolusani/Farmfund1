from django.db import models
from django.contrib.auth.models import User

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Farm(models.Model):
    crop_name = models.CharField(max_length=100)
    farm_name = models.CharField(max_length=100)
    crop_description = models.TextField()
    crop_budget = models.IntegerField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, default=1)  # Set a default user ID
    
    def __str__(self):
        return f"{self.farm_name} ({self.crop_name})"
    
class Income(models.Model):
    farm= models.ForeignKey(Farm, on_delete=models.CASCADE)
    amount = models.IntegerField()
    details = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_date = self.date.strftime('%d-%m-%Y')
        return f"{formatted_date}  {self.details}, Rs.{self.amount}/-"
    
class Expenditure(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    amount = models.IntegerField()
    details = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_date = self.date.strftime('%d-%m-%Y')
        return f"{formatted_date}  {self.details}, Rs.{self.amount}/-"
