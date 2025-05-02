from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, RangeFilter
from .models import Listing
from .serializers import ListingSerializer
from .pagination import CustomPageNumberPagination

class ListingFilter(FilterSet):
    price = RangeFilter()
    last_sold_price = RangeFilter()
    rent_price = RangeFilter()
    rentzestimate_amount = RangeFilter()
    tax_value = RangeFilter()
    zestimate_amount = RangeFilter()

    class Meta:
        model = Listing
        fields = {
            'bedrooms': ['exact'],
            'bathrooms': ['exact'],
            'home_type': ['exact'],
            'city': ['exact'],
            'state': ['exact'],
            'zipcode': ['exact'],
            'year_built': ['exact'],
            'tax_year': ['exact'],
        }

class ListingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows listings to be viewed.
    
    Pagination:
    - Results are paginated with 10 items per page by default
    - Use 'page' parameter to navigate pages
    - Use 'page_size' parameter to change number of items per page (max 100)
    
    Example:
    - GET /api/listings/?page=2&page_size=20
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ListingFilter
    search_fields = ['address', 'city', 'state', 'zipcode']
    ordering_fields = [
        'price', 'last_sold_price', 'rent_price', 'rentzestimate_amount',
        'tax_value', 'zestimate_amount', 'year_built', 'home_size',
        'property_size'
    ]
    ordering = ['-created_at']  # Default ordering
    pagination_class = CustomPageNumberPagination
