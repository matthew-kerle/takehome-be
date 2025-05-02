from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Listing
from .utils import format_price_from_cents


class ListingSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    last_sold_price = serializers.SerializerMethodField()
    rent_price = serializers.SerializerMethodField()
    rentzestimate_amount = serializers.SerializerMethodField()
    tax_value = serializers.SerializerMethodField()
    zestimate_amount = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            "id",
            "zillow_id",
            "area_unit",
            "bathrooms",
            "bedrooms",
            "home_size",
            "home_type",
            "last_sold_date",
            "last_sold_price",
            "link",
            "price",
            "property_size",
            "rent_price",
            "rentzestimate_amount",
            "rentzestimate_last_updated",
            "tax_value",
            "tax_year",
            "year_built",
            "zestimate_amount",
            "zestimate_last_updated",
            "address",
            "city",
            "state",
            "zipcode",
            "created_at",
            "updated_at",
            "last_imported_at",
            "data_hash",
        ]

    def get_price(self, obj):
        return format_price_from_cents(obj.price) if obj.price else None

    def get_last_sold_price(self, obj):
        return (
            format_price_from_cents(obj.last_sold_price)
            if obj.last_sold_price
            else None
        )

    def get_rent_price(self, obj):
        return format_price_from_cents(obj.rent_price) if obj.rent_price else None

    def get_rentzestimate_amount(self, obj):
        return (
            format_price_from_cents(obj.rentzestimate_amount)
            if obj.rentzestimate_amount
            else None
        )

    def get_tax_value(self, obj):
        return format_price_from_cents(obj.tax_value) if obj.tax_value else None

    def get_zestimate_amount(self, obj):
        return (
            format_price_from_cents(obj.zestimate_amount)
            if obj.zestimate_amount
            else None
        )
