from django.db.models import Q
from django_filters import filters as django_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import filters, viewsets

from .models import Listing
from .pagination import CustomPageNumberPagination
from .serializers import ListingSerializer
from .utils import convert_price_param_to_cents


class RangeFilterMixin:
    """Mixin to add min/max range filtering for numeric fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "filters"):
            self.filters = {}

    def create_range_filter(self, field_name, filter_name=None):
        """Create min/max filters for a numeric field."""
        if filter_name is None:
            filter_name = field_name

        self.filters[f"{filter_name}_min"] = django_filters.NumberFilter(
            field_name=field_name,
            lookup_expr="gte",
        )
        self.filters[f"{filter_name}_max"] = django_filters.NumberFilter(
            field_name=field_name,
            lookup_expr="lte",
        )


class PriceRangeFilterMixin:
    """Mixin to add price range filtering with currency conversion."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "filters"):
            self.filters = {}

    def create_price_range_filter(self, field_name, filter_name=None):
        """Create min/max filters for a price field with currency conversion."""
        if filter_name is None:
            filter_name = field_name

        self.filters[f"{filter_name}_min"] = django_filters.CharFilter(
            method=f"filter_{field_name}_min",
        )
        self.filters[f"{filter_name}_max"] = django_filters.CharFilter(
            method=f"filter_{field_name}_max",
        )

    def filter_price_range(self, queryset, field, min_value=None, max_value=None):
        """Filter queryset by price range.
        Uses a single Q object to combine min and max conditions.
        """
        if not min_value and not max_value:
            return queryset

        filters = Q()

        if min_value:
            min_cents = convert_price_param_to_cents(min_value)
            if min_cents is not None:
                filters &= Q(**{f"{field}__gte": min_cents})

        if max_value:
            max_cents = convert_price_param_to_cents(max_value)
            if max_cents is not None:
                filters &= Q(**{f"{field}__lte": max_cents})

        return queryset.filter(filters) if filters else queryset.none()


class ListingFilter(FilterSet, RangeFilterMixin, PriceRangeFilterMixin):
    """Filter for Listing model with support for range and price filtering."""

    # Address-related filters
    address = django_filters.CharFilter(lookup_expr="icontains")
    city = django_filters.CharFilter(lookup_expr="icontains")
    state = django_filters.CharFilter(lookup_expr="iexact")
    zipcode = django_filters.CharFilter(lookup_expr="icontains")

    bedrooms = django_filters.CharFilter(method="filter_bedrooms")
    bathrooms = django_filters.CharFilter(method="filter_bathrooms")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add range filters for numeric fields
        self.create_range_filter("home_size")
        self.create_range_filter("bedrooms")
        self.create_range_filter("bathrooms")
        self.create_range_filter("property_size")
        self.create_range_filter("year_built")

        # Add price range filters
        self.create_price_range_filter("price")
        self.create_price_range_filter("last_sold_price")
        self.create_price_range_filter("rent_price")
        self.create_price_range_filter("rentzestimate_amount")
        self.create_price_range_filter("tax_value")
        self.create_price_range_filter("zestimate_amount")

    def filter_price_min(self, queryset, name, value):
        return self.filter_price_range(queryset, "price", min_value=value)

    def filter_price_max(self, queryset, name, value):
        return self.filter_price_range(queryset, "price", max_value=value)

    def filter_last_sold_price_min(self, queryset, name, value):
        return self.filter_price_range(queryset, "last_sold_price", min_value=value)

    def filter_last_sold_price_max(self, queryset, name, value):
        return self.filter_price_range(queryset, "last_sold_price", max_value=value)

    def filter_rent_price_min(self, queryset, name, value):
        return self.filter_price_range(queryset, "rent_price", min_value=value)

    def filter_rent_price_max(self, queryset, name, value):
        return self.filter_price_range(queryset, "rent_price", max_value=value)

    def filter_rentzestimate_amount_min(self, queryset, name, value):
        field = "rentzestimate_amount"
        return self.filter_price_range(queryset, field, min_value=value)

    def filter_rentzestimate_amount_max(self, queryset, name, value):
        field = "rentzestimate_amount"
        return self.filter_price_range(queryset, field, max_value=value)

    def filter_tax_value_min(self, queryset, name, value):
        return self.filter_price_range(queryset, "tax_value", min_value=value)

    def filter_tax_value_max(self, queryset, name, value):
        return self.filter_price_range(queryset, "tax_value", max_value=value)

    def filter_zestimate_amount_min(self, queryset, name, value):
        return self.filter_price_range(queryset, "zestimate_amount", min_value=value)

    def filter_zestimate_amount_max(self, queryset, name, value):
        return self.filter_price_range(queryset, "zestimate_amount", max_value=value)

    def filter_bedrooms(self, queryset, name: str, value: str):
        """Filter by a single value or a comma-separated list of bedroom counts."""
        if not value:
            return queryset
        values = [v.strip() for v in value.split(",") if v.strip()]
        try:
            int_values = [int(v) for v in values]
        except ValueError:
            return queryset.none()
        return queryset.filter(bedrooms__in=int_values)

    def filter_bathrooms(self, queryset, name: str, value: str):
        """Filter by a single value or a comma-separated list of bathroom counts."""
        if not value:
            return queryset
        values = [v.strip() for v in value.split(",") if v.strip()]
        try:
            float_values = [float(v) for v in values]
        except ValueError:
            return queryset.none()
        return queryset.filter(bathrooms__in=float_values)

    class Meta:
        model = Listing
        fields = {
            "home_type": ["exact"],
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

    Price Filtering:
    Supports various price formats:
    - Plain numbers: price_min=500000 (500K)
    - K suffix: price_min=500K (500K)
    - M suffix: price_min=1.5M (1.5M)
    - Decimal points: price_min=1500.50 ($1,500.50)

    Examples:
    - GET /api/listings/?price_min=500K&price_max=2M
    - GET /api/listings/?price_min=1.5M
    - GET /api/listings/?rent_price_min=2.5K&rent_price_max=5K

    Address Filtering:
    - address: Case-insensitive partial match
    - city: Case-insensitive partial match
    - state: Case-insensitive exact match
    - zipcode: Case-insensitive partial match

    Examples:
    - GET /api/listings/?address=main
    - GET /api/listings/?city=san
    - GET /api/listings/?state=CA
    - GET /api/listings/?zipcode=94105

    Numeric Range Filtering:
    - home_size_min/max: Filter by home size range
    - bedrooms_min/max: Filter by number of bedrooms
    - bathrooms_min/max: Filter by number of bathrooms
    - property_size_min/max: Filter by property size range
    - year_built_min/max: Filter by year built range

    Examples:
    - GET /api/listings/?home_size_min=2000&home_size_max=3000
    - GET /api/listings/?bedrooms_min=3&bedrooms_max=4
    - GET /api/listings/?bathrooms_min=2&bathrooms_max=3
    """

    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ListingFilter
    search_fields = ["address", "city", "state", "zipcode"]
    ordering_fields = [
        "price",
        "last_sold_price",
        "rent_price",
        "rentzestimate_amount",
        "tax_value",
        "zestimate_amount",
        "year_built",
        "home_size",
        "property_size",
    ]
    ordering = ["-created_at"]  # Default ordering
    pagination_class = CustomPageNumberPagination
