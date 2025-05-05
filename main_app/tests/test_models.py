from django.test import TestCase
from django.contrib.auth.models import User
from main_app.models import Amenity, Property, Inquiry


class RealEstateModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='agent1', password='12345')

        self.pool = Amenity.objects.create(name='Swimming Pool')
        self.garden = Amenity.objects.create(name='Garden')

        self.property = Property.objects.create(
            title='Luxury Villa',
            type='villa',
            description='A spacious luxury villa.',
            price=1500000.00,
            size=500,
            rooms=5,
            bathrooms=4,
            user=self.user,
        )

        self.property.amenities.set([self.pool, self.garden])

        self.inquiry = Inquiry.objects.create(
            property=self.property,
            name='John Doe',
            email='john@example.com',
            phone='123456789',
            message='Is this villa still available?',
        )

  
    def test_amenity_str(self):
        self.assertEqual(str(self.pool), 'Swimming Pool')

    def test_property_str(self):
        self.assertEqual(str(self.property), 'Luxury Villa (villa)')

    def test_inquiry_str(self):
        self.assertEqual(str(self.inquiry), 'Inquiry from John Doe about Luxury Villa')

   
    def test_property_user_relationship(self):
        self.assertEqual(self.property.user.username, 'agent1')

    def test_property_amenities_relationship(self):
        self.assertEqual(self.property.amenities.count(), 2)
        self.assertIn(self.pool, self.property.amenities.all())
        self.assertIn(self.garden, self.property.amenities.all())

    def test_property_inquiry_relationship(self):
        self.assertEqual(self.inquiry.property, self.property)
        self.assertEqual(self.property.inquiries.count(), 1)
        self.assertEqual(self.property.inquiries.first().name, 'John Doe')

   
    def test_delete_property_cascades_to_inquiries(self):
        self.assertEqual(Inquiry.objects.count(), 1)
        self.property.delete()
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_delete_user_cascades_to_properties(self):
        self.assertEqual(Property.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Property.objects.count(), 0)
