from django.contrib import admin
from .models import Property, Amenity, Inquiry

class PropertyAdmin(admin.ModelAdmin):
    filter_horizontal = ('amenities',)

admin.site.register(Property, PropertyAdmin)
admin.site.register(Amenity)
admin.site.register(Inquiry)  