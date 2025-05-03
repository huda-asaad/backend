from django.urls import path
from .views import Home, PropertyIndex, PropertyDetailView


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('properties/', PropertyIndex.as_view(), name='property-index'),
    path('properties/<int:property_id>/', PropertyDetailView.as_view(), name='property-detail'),
]
