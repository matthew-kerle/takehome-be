from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Listing
import json

class ListingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test listings
        self.listing1 = Listing.objects.create(
            zillow_id="12345",
            area_unit="SqFt",
            bathrooms=2.5,
            bedrooms=3,
            home_size=2000,
            home_type="Single Family",
            last_sold_date="2020-01-15",
            last_sold_price=240000000,  # $2.4M
            link="https://www.zillow.com/homedetails/123",
            price=240000000,  # $2.4M
            property_size=5000,
            rent_price=300000,  # $3K
            rentzestimate_amount=385000,  # $3,850
            rentzestimate_last_updated="2024-01-01",
            tax_value=9586000,  # $95,860
            tax_year=2023,
            year_built=1990,
            zestimate_amount=100390600,  # $1,003,906
            zestimate_last_updated="2024-01-01",
            address="123 Main St",
            city="San Francisco",
            state="CA",
            zipcode="94105"
        )

        self.listing2 = Listing.objects.create(
            zillow_id="67890",
            area_unit="SqFt",
            bathrooms=1.5,
            bedrooms=2,
            home_size=1500,
            home_type="Condo",
            last_sold_date="2021-03-20",
            last_sold_price=150000000,  # $1.5M
            link="https://www.zillow.com/homedetails/456",
            price=150000000,  # $1.5M
            property_size=2000,
            rent_price=250000,  # $2.5K
            rentzestimate_amount=285000,  # $2,850
            rentzestimate_last_updated="2024-01-01",
            tax_value=7586000,  # $75,860
            tax_year=2023,
            year_built=1985,
            zestimate_amount=80390600,  # $803,906
            zestimate_last_updated="2024-01-01",
            address="456 Oak St",
            city="Oakland",
            state="CA",
            zipcode="94612"
        )

    def test_get_all_listings(self):
        """Test retrieving all listings"""
        url = reverse('listing-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)

    def test_get_single_listing(self):
        """Test retrieving a single listing"""
        url = reverse('listing-detail', args=[self.listing1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['zillow_id'], self.listing1.zillow_id)
        self.assertEqual(response.data['price'], "$2.4M")
        self.assertEqual(response.data['city'], "San Francisco")

    def test_get_nonexistent_listing(self):
        """Test retrieving a nonexistent listing"""
        url = reverse('listing-detail', args=[999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_bedrooms(self):
        """Test filtering listings by number of bedrooms"""
        url = reverse('listing-list')
        response = self.client.get(url, {'bedrooms': 3})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['bedrooms'], 3)

    def test_filter_by_city(self):
        """Test filtering listings by city"""
        url = reverse('listing-list')
        response = self.client.get(url, {'city': 'San Francisco'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['city'], "San Francisco")

    def test_filter_by_price_range(self):
        """Test filtering listings by price range"""
        url = reverse('listing-list')
        response = self.client.get(url, {
            'price_min': 100000000,  # $1M
            'price_max': 200000000   # $2M
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['price'], "$1.5M")

    def test_filter_by_multiple_criteria(self):
        """Test filtering listings by multiple criteria"""
        url = reverse('listing-list')
        response = self.client.get(url, {
            'bedrooms': 3,
            'city': 'San Francisco',
            'price_min': 200000000,  # $2M
            'price_max': 300000000   # $3M
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['price'], "$2.4M")

    def test_search_listings(self):
        """Test searching listings"""
        url = reverse('listing-list')
        response = self.client.get(url, {'search': 'San Francisco'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['city'], "San Francisco")

    def test_order_by_price_desc(self):
        """Test ordering listings by price (descending)"""
        url = reverse('listing-list')
        response = self.client.get(url, {'ordering': '-price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['price'], "$2.4M")
        self.assertEqual(response.data['results'][1]['price'], "$1.5M")

    def test_order_by_year_built(self):
        """Test ordering listings by year built"""
        url = reverse('listing-list')
        response = self.client.get(url, {'ordering': 'year_built'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['year_built'], 1985)
        self.assertEqual(response.data['results'][1]['year_built'], 1990)

    def test_pagination(self):
        """Test pagination of listings"""
        url = reverse('listing-list')
        response = self.client.get(url, {'page': 1, 'page_size': 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertTrue('next' in response.data)
        self.assertTrue('previous' in response.data)

    def test_invalid_page_number(self):
        """Test invalid page number"""
        url = reverse('listing-list')
        response = self.client.get(url, {'page': 999})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_invalid_page_size(self):
        """Test invalid page size"""
        url = reverse('listing-list')
        response = self.client.get(url, {'page_size': 999})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Should default to max page size

    def test_filter_by_home_type(self):
        """Test filtering listings by home type"""
        url = reverse('listing-list')
        response = self.client.get(url, {'home_type': 'Condo'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['home_type'], "Condo")

    def test_filter_by_state(self):
        """Test filtering listings by state"""
        url = reverse('listing-list')
        response = self.client.get(url, {'state': 'CA'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_zipcode(self):
        """Test filtering listings by zipcode"""
        url = reverse('listing-list')
        response = self.client.get(url, {'zipcode': '94105'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['zipcode'], "94105")

    def test_filter_by_tax_year(self):
        """Test filtering listings by tax year"""
        url = reverse('listing-list')
        response = self.client.get(url, {'tax_year': 2023})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_rent_price_range(self):
        """Test filtering listings by rent price range"""
        url = reverse('listing-list')
        response = self.client.get(url, {
            'rent_price_min': 250000,  # $2.5K
            'rent_price_max': 350000   # $3.5K
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_zestimate_range(self):
        """Test filtering listings by zestimate range"""
        url = reverse('listing-list')
        response = self.client.get(url, {
            'zestimate_amount_min': 80000000,  # $800K
            'zestimate_amount_max': 120000000  # $1.2M
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_combined_filters_and_ordering(self):
        """Test combining filters with ordering"""
        url = reverse('listing-list')
        response = self.client.get(url, {
            'state': 'CA',
            'ordering': '-price',
            'page_size': 1
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['price'], "$2.4M")
