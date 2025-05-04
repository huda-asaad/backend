from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Property, Amenity,  Inquiry
from .serializers import PropertySerializer, AmenitySerializer
from .serializers import InquirySerializer


class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the Aqar API home route!'}
        return Response(content)


class PropertyIndex(APIView):
    serializer_class = PropertySerializer

    def get(self, request):
        try:
            queryset = Property.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PropertyDetailView(APIView):
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

            # print(" Serializer Errors:", serializer.errors)
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

            # تحقق إن كان فيه amenity بنفس الاسم، أو أنشئ جديد
            amenity, created = Amenity.objects.get_or_create(name=amenity_name)

            # أضف العلاقة إذا لم تكن موجودة
            property_instance.amenities.add(amenity)

            # أرجع القائمة المحدثة
            amenities = property_instance.amenities.all()
            serializer = AmenitySerializer(amenities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Property.DoesNotExist:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class InquiryCreateView(APIView):
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