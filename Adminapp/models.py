from django.db import models

# Create your models here.

#Category section
class LocationDB(models.Model):
    Location = models.CharField(max_length=120, blank=True,null=True)

    def __str__(self):
        return self.Location




#Location section
class CategoryDB(models.Model):
    Category_Name = models.CharField(max_length=100, blank=True,null=True)
    Category_Image = models.ImageField(upload_to="category", null=True, blank=True)


