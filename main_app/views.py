from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Property, Amenity, Inquiry
from .serializers import  PropertySerializer, AmenitySerializer,   InquirySerializer,  UserSerializer
from django.contrib.auth import authenticate
from rest_framework import generics, status, permissions
from django.db import IntegrityError
from django.core.exceptions import ValidationError



class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the Aqar API home route!'}
        return Response(content)


# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    try:
      print(request.data, "checking user data from react")
      response = super().create(request, *args, **kwargs)
      user = User.objects.get(username=response.data['username'])
    #   user.is_staff = True 
      refresh = RefreshToken.for_user(user)
      content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data }
      return Response(content, status=status.HTTP_200_OK)
    except (ValidationError, IntegrityError) as err:
      return Response({ 'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):

  def post(self, request):
    try:
      username = request.data.get('username')
      password = request.data.get('password')
      user = authenticate(username=username, password=password)
      if user:
        refresh = RefreshToken.for_user(user)
        content = {'refresh': str(refresh), 'access': str(refresh.access_token),'user': UserSerializer(user).data}
        return Response(content, status=status.HTTP_200_OK)
      return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    try:
      user = User.objects.get(username=request.user.username)
      try:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),'access': str(refresh.access_token),'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
      except Exception as token_error:
        return Response({"detail": "Failed to generate token.", "error": str(token_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
      print(str(err))
      return Response({"detail": "Unexpected error occurred.", "error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PropertyIndex(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertySerializer

    def get(self, request):
        try:
            queryset = Property.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(user_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PropertyDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertySerializer

    def get(self, request, property_id):
        try:
            property_obj = get_object_or_404(Property, id=property_id)
            serializer = self.serializer_class(property_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, property_id):
        try:
            property_obj = get_object_or_404(Property, id=property_id)
            data = request.data.copy()

            if 'image' not in data or not data.get('image') or data.get('image') in ["null", "undefined", ""]:
                data.pop('image', None)

            serializer = self.serializer_class(property_obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)


            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, property_id):
        try:
            property_obj = get_object_or_404(Property, id=property_id)
            property_obj.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AmenitiesIndex(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AmenitySerializer
    def get(self, request, property_id):
        try:
            property_instance = Property.objects.get(id=property_id)
            amenities = property_instance.amenities.all()
            serializer = AmenitySerializer(amenities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Property.DoesNotExist:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, property_id):
        try:
            property_instance = Property.objects.get(id=property_id)
            amenity_name = request.data.get('name')

            if not amenity_name:
                return Response({'error': 'Amenity name is required'}, status=status.HTTP_400_BAD_REQUEST)

            amenity, created = Amenity.objects.get_or_create(name=amenity_name)

            property_instance.amenities.add(amenity)

            amenities = property_instance.amenities.all()
            serializer = AmenitySerializer(amenities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Property.DoesNotExist:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class InquiryCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InquirySerializer

    def post(self, request, property_id):
        try:

            property_obj = get_object_or_404(Property, id=property_id)
            
            data = request.data.copy()
            data['property'] = property_obj.id

            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)