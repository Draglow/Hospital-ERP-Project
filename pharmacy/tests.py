from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Medicine

User = get_user_model()

class MobilePharmacyViewTests(TestCase):
    """Test cases for mobile pharmacy views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

        # Create test medicines
        self.medicine1 = Medicine.objects.create(
            name='Test Medicine 1',
            generic_name='Generic 1',
            manufacturer='Test Manufacturer',
            category='antibiotic',
            form='tablet',
            strength='500mg',
            stock_quantity=100,
            minimum_stock_level=20,
            unit_price=10.00,
            cost_price=8.00,
            expiry_date=timezone.now().date() + timedelta(days=365)
        )

        # Low stock medicine
        self.medicine2 = Medicine.objects.create(
            name='Low Stock Medicine',
            generic_name='Generic 2',
            manufacturer='Test Manufacturer',
            category='painkiller',
            form='tablet',
            strength='250mg',
            stock_quantity=5,  # Below minimum
            minimum_stock_level=20,
            unit_price=15.00,
            cost_price=12.00,
            expiry_date=timezone.now().date() + timedelta(days=365)
        )

        # Expiring soon medicine
        self.medicine3 = Medicine.objects.create(
            name='Expiring Medicine',
            generic_name='Generic 3',
            manufacturer='Test Manufacturer',
            category='vitamin',
            form='capsule',
            strength='100mg',
            stock_quantity=50,
            minimum_stock_level=10,
            unit_price=20.00,
            cost_price=16.00,
            expiry_date=timezone.now().date() + timedelta(days=15)  # Expiring soon
        )

    def test_mobile_pharmacy_list_view(self):
        """Test mobile pharmacy list view loads correctly"""
        url = reverse('pharmacy:medicine_list') + '?mobile=1'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'mobile-stats-grid')
        self.assertContains(response, 'Total Medicines')
        self.assertContains(response, 'New This Month')
        self.assertContains(response, 'Low Stock')
        self.assertContains(response, 'Expiring Soon')

    def test_mobile_pharmacy_statistics(self):
        """Test mobile pharmacy statistics are calculated correctly"""
        url = reverse('pharmacy:medicine_list') + '?mobile=1'
        response = self.client.get(url)

        # Check context variables
        self.assertEqual(response.context['total_medicines'], 3)
        self.assertEqual(response.context['low_stock_count'], 1)  # medicine2
        self.assertEqual(response.context['expiring_soon_count'], 1)  # medicine3

    def test_mobile_template_used(self):
        """Test that mobile template is used when mobile=1 parameter is present"""
        url = reverse('pharmacy:medicine_list') + '?mobile=1'
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'pharmacy/mobile_list.html')

    def test_desktop_template_used(self):
        """Test that desktop template is used when mobile parameter is not present"""
        url = reverse('pharmacy:medicine_list')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'pharmacy/list.html')
