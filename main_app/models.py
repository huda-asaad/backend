from django.db import models


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    def __str__(self):
        return self.name



class Property(models.Model):
    PROPERTY_TYPES = [
        ('villa', 'Villa'),
        ('apartment', 'Apartment'),
    ]

    title = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    size = models.PositiveIntegerField(help_text="Size in square meters (م²)")
    rooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)

    amenities = models.ManyToManyField(Amenity, blank=True)

    def __str__(self):
        return f"{self.title} ({self.type})"


class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name} about {self.property.title}"
