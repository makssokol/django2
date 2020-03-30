from django.db import models

# Create your models here.
class ArtCategory(models.Model):
    name = models.CharField(verbose_name="name", max_length=64, unique=True)
    description = models.TextField(verbose_name="description", blank=True)
    is_active = models.BooleanField(verbose_name="category is active", default=True)

    def __str__(self):
        return self.name

class ArtObject(models.Model):
    category = models.ForeignKey(ArtCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="artobject name", max_length=128)
    image = models.ImageField(upload_to="art_images", blank=True)
    artist = models.CharField(verbose_name="author", max_length=60, blank=True)
    description = models.TextField(verbose_name="artobject description", blank=True)
    price = models.DecimalField(verbose_name="price", max_digits=12, decimal_places=2, default=0)
    location = models.CharField(verbose_name="location", max_length=128)
    is_active = models.BooleanField(verbose_name="art object is active", default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Contact(models.Model):
    phone = models.CharField(max_length=50, verbose_name="phone number")
    email = models.EmailField(max_length=254, verbose_name="email")
    city = models.CharField(max_length=128, verbose_name="city")
    address = models.CharField(max_length=254, verbose_name="address")

    def __str__(self):
        return f"{self.pk} {self.email}"
    
