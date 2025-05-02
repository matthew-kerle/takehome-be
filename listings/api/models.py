from django.db import models
from django.utils import timezone
import hashlib
import json
from datetime import datetime

class Listing(models.Model):
    area_unit = models.CharField(max_length=10)
    bathrooms = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    bedrooms = models.IntegerField(null=True)
    home_size = models.IntegerField(null=True)
    home_type = models.CharField(max_length=50)
    last_sold_date = models.DateField(null=True)
    last_sold_price = models.IntegerField(null=True)  # Stored in cents
    link = models.URLField(max_length=500)
    price = models.BigIntegerField(null=True)  # Stored in cents
    property_size = models.IntegerField(null=True)
    rent_price = models.IntegerField(null=True)  # Stored in cents
    rentzestimate_amount = models.IntegerField(null=True)  # Stored in cents
    rentzestimate_last_updated = models.DateField(null=True)
    tax_value = models.IntegerField(null=True)  # Stored in cents
    tax_year = models.IntegerField(null=True)
    year_built = models.IntegerField(null=True)
    zestimate_amount = models.IntegerField(null=True)  # Stored in cents
    zestimate_last_updated = models.DateField(null=True)
    zillow_id = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    
    # New timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_imported_at = models.DateTimeField(null=True)
    
    # Hash field for change detection
    data_hash = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.address} - ${self.price/100:,.2f}" if self.price else self.address

    def calculate_data_hash(self):
        """Calculate a hash of the relevant fields to detect changes."""
        fields_to_hash = [
            str(self.area_unit),
            str(self.bathrooms),
            str(self.bedrooms),
            str(self.home_size),
            str(self.home_type),
            str(self.last_sold_date),
            str(self.last_sold_price),
            str(self.link),
            str(self.price),
            str(self.property_size),
            str(self.rent_price),
            str(self.rentzestimate_amount),
            str(self.rentzestimate_last_updated),
            str(self.tax_value),
            str(self.tax_year),
            str(self.year_built),
            str(self.zestimate_amount),
            str(self.zestimate_last_updated),
            str(self.zillow_id),
            str(self.address),
            str(self.city),
            str(self.state),
            str(self.zipcode),
        ]
        return hashlib.sha256(''.join(fields_to_hash).encode()).hexdigest()

    def save(self, *args, **kwargs):
        self.data_hash = self.calculate_data_hash()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-zestimate_amount']
