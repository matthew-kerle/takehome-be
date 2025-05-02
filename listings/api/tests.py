import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Listing
from .utils import convert_price_param_to_cents, convert_price_to_cents


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
            zipcode="94105",
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
            zipcode="94612",
        )

        self.listing3 = Listing.objects.create(
            zillow_id="11111",
            area_unit="SqFt",
            bathrooms=3.0,
            bedrooms=4,
            home_size=2500,
            home_type="Single Family",
            last_sold_date="2022-01-15",
            last_sold_price=350000000,  # $3.5M
            link="https://www.zillow.com/homedetails/789",
            price=400000000,  # $4M
            property_size=6000,
            rent_price=500000,  # $5K
            rentzestimate_amount=485000,  # $4,850
            rentzestimate_last_updated="2024-01-01",
            tax_value=12586000,  # $125,860
            tax_year=2023,
            year_built=2000,
            zestimate_amount=420390600,  # $4,203,906
            zestimate_last_updated="2024-01-01",
            address="789 Pine St",
            city="San Francisco",
            state="CA",
            zipcode="94105",
        )

        self.listing4 = Listing.objects.create(
            zillow_id="22222",
            area_unit="SqFt",
            bathrooms=2.0,
            bedrooms=3,
            home_size=1800,
            home_type="Single Family",
            last_sold_date="2021-06-15",
            last_sold_price=280000000,  # $2.8M
            link="https://www.zillow.com/homedetails/101",
            price=300000000,  # $3M
            property_size=4000,
            rent_price=None,  # No rent price
            rentzestimate_amount=None,
            rentzestimate_last_updated=None,
            tax_value=9586000,
            tax_year=2023,
            year_built=1995,
            zestimate_amount=320390600,
            zestimate_last_updated="2024-01-01",
            address="101 Market St",
            city="San Francisco",
            state="CA",
            zipcode="94105",
        )

    def test_get_all_listings(self):
        """Test retrieving all listings"""
        url = reverse("listing-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)
        self.assertEqual(response.data["count"], 4)

    def test_get_single_listing(self):
        """Test retrieving a single listing"""
        url = reverse("listing-detail", args=[self.listing1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["zillow_id"], self.listing1.zillow_id)
        self.assertEqual(response.data["price"], "$2.4M")
        self.assertEqual(response.data["city"], "San Francisco")

    def test_get_nonexistent_listing(self):
        """Test retrieving a nonexistent listing"""
        url = reverse("listing-detail", args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_bedrooms(self):
        """Test filtering listings by number of bedrooms"""
        url = reverse("listing-list")
        response = self.client.get(url, {"bedrooms": 3})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["bedrooms"], 3)
        self.assertEqual(response.data["results"][1]["bedrooms"], 3)

    def test_filter_by_city(self):
        """Test filtering listings by city"""
        url = reverse("listing-list")
        response = self.client.get(url, {"city": "San Francisco"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["city"], "San Francisco")
        self.assertEqual(response.data["results"][1]["city"], "San Francisco")

    def test_filter_by_price_range(self):
        """Test filtering listings by price range"""
        url = reverse("listing-list")

        # Test exact price range
        response = self.client.get(url, {"price_min": "1.4M", "price_max": "1.6M"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify count matches filtered results
        filtered_count = Listing.objects.filter(
            price__gte=convert_price_to_cents("1.4M"),
            price__lte=convert_price_to_cents("1.6M"),
        ).count()
        self.assertEqual(response.data["count"], filtered_count)

        # Verify all returned results are within the price range
        min_price_cents = convert_price_to_cents("1.4M")
        max_price_cents = convert_price_to_cents("1.6M")
        for item in response.data["results"]:
            price_cents = convert_price_to_cents(item["price"])
            self.assertGreaterEqual(price_cents, min_price_cents)
            self.assertLessEqual(price_cents, max_price_cents)

        # Test wider price range
        response = self.client.get(url, {"price_min": "2M", "price_max": "5M"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify count matches filtered results
        filtered_count = Listing.objects.filter(
            price__gte=convert_price_to_cents("2M"),
            price__lte=convert_price_to_cents("5M"),
        ).count()
        self.assertEqual(response.data["count"], filtered_count)

        # Verify all returned results are within the price range
        min_price_cents = convert_price_to_cents("2M")
        max_price_cents = convert_price_to_cents("5M")
        for item in response.data["results"]:
            price_cents = convert_price_to_cents(item["price"])
            self.assertGreaterEqual(price_cents, min_price_cents)
            self.assertLessEqual(price_cents, max_price_cents)

    def test_filter_by_multiple_criteria(self):
        """Test filtering listings by multiple criteria"""
        url = reverse("listing-list")
        response = self.client.get(
            url,
            {
                "bedrooms": 3,
                "city": "San Francisco",
                "price_min": "2M",
                "price_max": "3M",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify count matches filtered results
        filtered_qs = Listing.objects.filter(
            bedrooms=3,
            city="San Francisco",
            price__gte=convert_price_to_cents("2M"),
            price__lte=convert_price_to_cents("3M"),
        )
        self.assertEqual(response.data["count"], filtered_qs.count())

        # Verify all returned results match all criteria
        for item in response.data["results"]:
            self.assertEqual(item["bedrooms"], 3)
            self.assertEqual(item["city"], "San Francisco")
            price_cents = convert_price_to_cents(item["price"])
            self.assertGreaterEqual(price_cents, convert_price_to_cents("2M"))
            self.assertLessEqual(price_cents, convert_price_to_cents("3M"))

    def test_search_listings(self):
        """Test searching listings"""
        url = reverse("listing-list")
        response = self.client.get(url, {"search": "San Francisco"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["city"], "San Francisco")
        self.assertEqual(response.data["results"][1]["city"], "San Francisco")

    def test_order_by_price_desc(self):
        """Test ordering listings by price (descending)"""
        url = reverse("listing-list")
        response = self.client.get(url, {"ordering": "-price"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)
        self.assertEqual(response.data["results"][0]["price"], "$4M")
        self.assertEqual(response.data["results"][1]["price"], "$3.5M")
        self.assertEqual(response.data["results"][2]["price"], "$2.4M")
        self.assertEqual(response.data["results"][3]["price"], "$1.5M")

    def test_order_by_year_built(self):
        """Test ordering listings by year built"""
        url = reverse("listing-list")
        response = self.client.get(url, {"ordering": "year_built"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)
        self.assertEqual(response.data["results"][0]["year_built"], 1985)
        self.assertEqual(response.data["results"][1]["year_built"], 1990)
        self.assertEqual(response.data["results"][2]["year_built"], 1995)
        self.assertEqual(response.data["results"][3]["year_built"], 2000)

    def test_pagination(self):
        """Test pagination of listings"""
        url = reverse("listing-list")
        response = self.client.get(url, {"page": 1, "page_size": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertTrue("next" in response.data)
        self.assertTrue("previous" in response.data)

    def test_invalid_page_number(self):
        """Test invalid page number"""
        url = reverse("listing-list")
        response = self.client.get(url, {"page": 999})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_invalid_page_size(self):
        """Test invalid page size"""
        url = reverse("listing-list")
        response = self.client.get(url, {"page_size": 999})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 4
        )  # Should default to max page size

    def test_filter_by_home_type(self):
        """Test filtering listings by home type"""
        url = reverse("listing-list")
        response = self.client.get(url, {"home_type": "Condo"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["home_type"], "Condo")

    def test_filter_by_state(self):
        """Test filtering listings by state"""
        url = reverse("listing-list")
        response = self.client.get(url, {"state": "CA"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)

    def test_filter_by_zipcode(self):
        """Test filtering listings by zipcode"""
        url = reverse("listing-list")
        response = self.client.get(url, {"zipcode": "94105"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["zipcode"], "94105")
        self.assertEqual(response.data["results"][1]["zipcode"], "94105")

    def test_filter_by_tax_year(self):
        """Test filtering listings by tax year"""
        url = reverse("listing-list")
        response = self.client.get(url, {"tax_year": 2023})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)

    def test_filter_by_rent_price_range(self):
        """Test filtering listings by rent price range"""
        url = reverse("listing-list")

        # Test with rent price range 2.5K to 4K
        response = self.client.get(
            url, {"rent_price_min": "2.5K", "rent_price_max": "4K"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]

        # Verify all returned listings have rent prices in the range
        for listing in results:
            rent_price = listing.get("rent_price")
            if rent_price is not None:  # Skip listings with no rent price
                cents = convert_price_to_cents(rent_price)
                self.assertGreaterEqual(cents, convert_price_to_cents("2.5K"))
                self.assertLessEqual(cents, convert_price_to_cents("4K"))

        # Verify listings outside the range are not included
        self.assertFalse(any(listing.get("rent_price") == "$5K" for listing in results))

    def test_filter_by_zestimate_range(self):
        """Test filtering listings by zestimate range"""
        url = reverse("listing-list")
        response = self.client.get(
            url,
            {
                "zestimate_amount_min": "800K",  # $800K
                "zestimate_amount_max": "1.2M",  # $1.2M
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_by_last_sold_price_range(self):
        """Test filtering listings by last sold price range"""
        url = reverse("listing-list")
        response = self.client.get(
            url,
            {"last_sold_price_min": "2M", "last_sold_price_max": "3M"},  # $2M  # $3M
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["last_sold_price"], "$2.4M")

    def test_filter_by_tax_value_range(self):
        """Test filtering listings by tax value range"""
        url = reverse("listing-list")
        response = self.client.get(
            url, {"tax_value_min": "90K", "tax_value_max": "100K"}  # $90K  # $100K
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["tax_value"], "$95,860")

    def test_filter_by_price_formats(self):
        """Test filtering listings using different price formats"""
        url = reverse("listing-list")

        # Test K suffix
        response = self.client.get(url, {"price_min": "1.5K", "price_max": "2.5M"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["price"], "$2.4M")

        # Test M suffix
        response = self.client.get(url, {"price_min": "1M", "price_max": "3M"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)
        prices = [item["price"] for item in response.data["results"]]
        self.assertTrue("$1.5M" in prices)
        self.assertTrue("$2.4M" in prices)

        # Test decimal points
        response = self.client.get(
            url, {"price_min": "1500000.50", "price_max": "2500000.75"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["price"], "$2.4M")

        # Test plain numbers
        response = self.client.get(url, {"price_min": 1500000, "price_max": 2500000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["price"], "$2.4M")

    def test_filter_by_invalid_price_formats(self):
        """Test filtering listings with invalid price formats"""
        url = reverse("listing-list")

        # Test invalid suffix
        response = self.client.get(url, {"price_min": "1.5X", "price_max": "2.5Y"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

        # Test invalid numbers
        response = self.client.get(url, {"price_min": "abc", "price_max": "def"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

        # Test mixed valid/invalid
        response = self.client.get(url, {"price_min": "1.5M", "price_max": "invalid"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_filter_by_rent_price_with_k_suffix(self):
        """Test filtering listings by rent price using K suffix"""
        url = reverse("listing-list")
        response = self.client.get(
            url, {"rent_price_min": "2.5K", "rent_price_max": "4K"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        rent_prices = [item["rent_price"] for item in response.data["results"]]
        self.assertTrue("$2.5K" in rent_prices)
        self.assertTrue("$3K" in rent_prices)

    def test_price_range_filtering(self):
        """Test price range filtering with various ranges"""
        url = reverse("listing-list")

        # Test range that should match only listing2 ($1.5M)
        response = self.client.get(url, {"price_min": "1.4M", "price_max": "1.6M"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["price"], "$1.5M")

        # Test range that should match listing1 ($2.4M) and listing2 ($1.5M)
        response = self.client.get(url, {"price_min": "1.4M", "price_max": "2.5M"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        prices = [item["price"] for item in response.data["results"]]
        self.assertTrue("$1.5M" in prices)
        self.assertTrue("$2.4M" in prices)

        # Test range that should match all listings
        response = self.client.get(url, {"price_min": "1M", "price_max": "5M"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)

        # Test range that should match no listings
        response = self.client.get(url, {"price_min": "5M", "price_max": "10M"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

        # Test range that should match only listing3 ($4M)
        response = self.client.get(url, {"price_min": "3.5M", "price_max": "4.5M"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["price"], "$4.0M")

    def test_count_reflects_filtered_results(self):
        """Test that the count reflects the number of filtered results"""
        url = reverse("listing-list")

        # Test with no filters - should show all listings
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Listing.objects.count())

        # Test with city filter
        response = self.client.get(url, {"city": "San Francisco"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_count = Listing.objects.filter(city="San Francisco").count()
        self.assertEqual(response.data["count"], filtered_count)

        # Test with price range filter
        response = self.client.get(url, {"price_min": "2M", "price_max": "3M"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_count = Listing.objects.filter(
            price__gte=convert_price_to_cents("2M"),
            price__lte=convert_price_to_cents("3M"),
        ).count()
        self.assertEqual(response.data["count"], filtered_count)

        # Test with multiple filters
        response = self.client.get(
            url,
            {
                "city": "San Francisco",
                "bedrooms": 3,
                "price_min": "2M",
                "price_max": "3M",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_count = Listing.objects.filter(
            city="San Francisco",
            bedrooms=3,
            price__gte=convert_price_to_cents("2M"),
            price__lte=convert_price_to_cents("3M"),
        ).count()
        self.assertEqual(response.data["count"], filtered_count)

    def test_filter_by_home_size_range(self):
        """Test filtering listings by home size range"""
        url = reverse("listing-list")

        # Test with home size range 2000-3000 sq ft
        response = self.client.get(url, {"home_size_min": 2000, "home_size_max": 3000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify all returned listings have home size in the range
        for listing in response.data["results"]:
            home_size = listing.get("home_size")
            if home_size is not None:  # Skip listings with no home size
                self.assertGreaterEqual(home_size, 2000)
                self.assertLessEqual(home_size, 3000)

        # Verify count matches filtered results
        filtered_count = Listing.objects.filter(
            home_size__gte=2000, home_size__lte=3000
        ).count()
        self.assertEqual(response.data["count"], filtered_count)

    def test_filter_by_bedrooms_range(self):
        """Test filtering listings by bedrooms range"""
        url = reverse("listing-list")

        # Test with bedrooms range 3-4
        response = self.client.get(url, {"bedrooms_min": 3, "bedrooms_max": 4})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify all returned listings have bedrooms in the range
        for listing in response.data["results"]:
            bedrooms = listing.get("bedrooms")
            if bedrooms is not None:  # Skip listings with no bedrooms
                self.assertGreaterEqual(bedrooms, 3)
                self.assertLessEqual(bedrooms, 4)

        # Verify count matches filtered results
        filtered_count = Listing.objects.filter(
            bedrooms__gte=3, bedrooms__lte=4
        ).count()
        self.assertEqual(response.data["count"], filtered_count)

    def test_filter_by_bathrooms_range(self):
        """Test filtering listings by bathrooms range"""
        url = reverse("listing-list")

        # Test with bathrooms range 2-3
        response = self.client.get(url, {"bathrooms_min": 2, "bathrooms_max": 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify all returned listings have bathrooms in the range
        for listing in response.data["results"]:
            bathrooms = listing.get("bathrooms")
            if bathrooms is not None:  # Skip listings with no bathrooms
                self.assertGreaterEqual(bathrooms, 2)
                self.assertLessEqual(bathrooms, 3)

        # Verify count matches filtered results
        filtered_count = Listing.objects.filter(
            bathrooms__gte=2, bathrooms__lte=3
        ).count()
        self.assertEqual(response.data["count"], filtered_count)

    def test_filter_by_property_size_range(self):
        """Test filtering listings by property size range"""
        url = reverse("listing-list")

        # Test with property size range 5000-10000 sq ft
        response = self.client.get(
            url, {"property_size_min": 5000, "property_size_max": 10000}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify all returned listings have property size in the range
        for listing in response.data["results"]:
            property_size = listing.get("property_size")
            if property_size is not None:  # Skip listings with no property size
                self.assertGreaterEqual(property_size, 5000)
                self.assertLessEqual(property_size, 10000)

        # Verify count matches filtered results
        filtered_count = Listing.objects.filter(
            property_size__gte=5000, property_size__lte=10000
        ).count()
        self.assertEqual(response.data["count"], filtered_count)

    def test_filter_by_multiple_numeric_ranges(self):
        """Test filtering listings by multiple numeric ranges"""
        url = reverse("listing-list")

        # Test with multiple range filters
        response = self.client.get(
            url,
            {
                "home_size_min": 2000,
                "home_size_max": 3000,
                "bedrooms_min": 3,
                "bedrooms_max": 4,
                "bathrooms_min": 2,
                "bathrooms_max": 3,
                "property_size_min": 5000,
                "property_size_max": 10000,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify all returned listings match all range criteria
        for listing in response.data["results"]:
            home_size = listing.get("home_size")
            bedrooms = listing.get("bedrooms")
            bathrooms = listing.get("bathrooms")
            property_size = listing.get("property_size")

            if home_size is not None:
                self.assertGreaterEqual(home_size, 2000)
                self.assertLessEqual(home_size, 3000)

            if bedrooms is not None:
                self.assertGreaterEqual(bedrooms, 3)
                self.assertLessEqual(bedrooms, 4)

            if bathrooms is not None:
                self.assertGreaterEqual(bathrooms, 2)
                self.assertLessEqual(bathrooms, 3)

            if property_size is not None:
                self.assertGreaterEqual(property_size, 5000)
                self.assertLessEqual(property_size, 10000)

        # Verify count matches filtered results
        filtered_count = Listing.objects.filter(
            home_size__gte=2000,
            home_size__lte=3000,
            bedrooms__gte=3,
            bedrooms__lte=4,
            bathrooms__gte=2,
            bathrooms__lte=3,
            property_size__gte=5000,
            property_size__lte=10000,
        ).count()
        self.assertEqual(response.data["count"], filtered_count)
