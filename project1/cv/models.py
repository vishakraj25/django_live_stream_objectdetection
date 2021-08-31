from django.db import models
# Create your models here.

class Users(models.Model):
    email = models.EmailField(max_length = 254)    
    password = models.CharField(max_length=100)

    def __str__(self):
        return(self.email)


class Datatable(models.Model):
    classes = models.CharField(max_length = 254)    
    date_d = models.DateField()

    def __str__(self):
        return(str(self.date_d)+str(self.classes))
