from django.urls import path
from . import views
from .views import AmenitiesIndex, InquiryCreateView, CreateUserView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView  # استيراد View الخاص بتجديد التوكن


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('properties/', views.PropertyIndex.as_view(), name='property-index'),
    path('properties/<int:property_id>/', views.PropertyDetailView.as_view(), name='property-detail'),
    path('properties/<int:property_id>/amenities/', AmenitiesIndex.as_view(), name='amenities-list'),
    path('properties/<int:property_id>/inquiries/', InquiryCreateView.as_view(), name='create-inquiry'),
    path('users/signup/', CreateUserView.as_view(), name='signup'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', views.VerifyUserView.as_view(), name='token_refresh'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # استخدام TokenRefreshView من simplejwt

]

