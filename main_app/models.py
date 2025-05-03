from django.db import models



    


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
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)  # ✅ أضف هذا السطر

    def __str__(self):
        return f"{self.title} ({self.type})"


