import csv
import os
from datetime import date, datetime
from typing import Any, Dict, Optional

from api.models import Listing
from api.utils import convert_price_to_cents
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date


def parse_date_safely(value: Optional[str]) -> Optional[date]:
    """Parse a date string safely, returning None for invalid inputs."""
    if not value:
        return None
    try:
        return parse_date(value)
    except (ValueError, TypeError):
        return None


class Command(BaseCommand):
    help = "Import listing data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete all existing records before import",
        )

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        if options["reset"]:
            Listing.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS("Successfully deleted all existing listings")
            )

        csv_file = os.path.join("sample-data", "data_with_rent.csv")
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file}"))
            return

        with open(csv_file, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Clean up column names and values
                row = {k.strip(): v.strip() if v else None for k, v in row.items()}

                # Convert date strings to date objects
                last_sold_date = parse_date_safely(row.get("last_sold_date"))
                rentzestimate_last_updated = parse_date_safely(
                    row.get("rentzestimate_last_updated")
                )
                zestimate_last_updated = parse_date_safely(
                    row.get("zestimate_last_updated")
                )

                # Convert numeric strings to integers or None
                def safe_int(value: Optional[str]) -> Optional[int]:
                    if not value:
                        return None
                    try:
                        return int(value)
                    except (ValueError, TypeError):
                        return None

                def safe_decimal(value: Optional[str]) -> Optional[float]:
                    try:
                        return float(value) if value else None
                    except (ValueError, TypeError):
                        return None

                # Convert prices using the proper conversion function
                price = convert_price_to_cents(row.get("price"))
                last_sold_price = convert_price_to_cents(row.get("last_sold_price"))
                rent_price = convert_price_to_cents(row.get("rent_price"))
                rentzestimate_amount = convert_price_to_cents(
                    row.get("rentzestimate_amount")
                )
                tax_value = convert_price_to_cents(row.get("tax_value"))
                zestimate_amount = convert_price_to_cents(row.get("zestimate_amount"))

                # Debug logging for price conversions
                self.stdout.write(
                    self.style.SUCCESS(f'Converting prices for {row.get("zillow_id")}:')
                )
                self.stdout.write(f'  Original price: {row.get("price")} -> {price}')
                self.stdout.write(
                    f"  Original last_sold_price: "
                    f'{row.get("last_sold_price")} -> {last_sold_price}'
                )
                self.stdout.write(
                    f"  Original rent_price: "
                    f'{row.get("rent_price")} -> {rent_price}'
                )
                self.stdout.write(
                    f"  Original rentzestimate_amount: "
                    f'{row.get("rentzestimate_amount")} -> {rentzestimate_amount}'
                )
                self.stdout.write(
                    f"  Original tax_value: " f'{row.get("tax_value")} -> {tax_value}'
                )
                self.stdout.write(
                    f"  Original zestimate_amount: "
                    f'{row.get("zestimate_amount")} -> {zestimate_amount}'
                )

                try:
                    listing, created = Listing.objects.update_or_create(
                        zillow_id=row["zillow_id"],
                        defaults={
                            "area_unit": row.get("area_unit"),
                            "bathrooms": safe_decimal(row.get("bathrooms")),
                            "bedrooms": safe_int(row.get("bedrooms")),
                            "home_size": safe_int(row.get("home_size")),
                            "home_type": row.get("home_type"),
                            "last_sold_date": last_sold_date,
                            "last_sold_price": last_sold_price,
                            "link": row.get("link"),
                            "price": price,
                            "property_size": safe_int(row.get("property_size")),
                            "rent_price": rent_price,
                            "rentzestimate_amount": rentzestimate_amount,
                            "rentzestimate_last_updated": rentzestimate_last_updated,
                            "tax_value": tax_value,
                            "tax_year": safe_int(row.get("tax_year")),
                            "year_built": safe_int(row.get("year_built")),
                            "zestimate_amount": zestimate_amount,
                            "zestimate_last_updated": zestimate_last_updated,
                            "address": row.get("address"),
                            "city": row.get("city"),
                            "state": row.get("state"),
                            "zipcode": row.get("zipcode"),
                            "last_imported_at": datetime.now(),
                        },
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Created new listing: {listing.zillow_id}"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Updated existing listing: {listing.zillow_id}"
                            )
                        )
                    # Calculate and save the data hash
                    listing.data_hash = listing.calculate_data_hash()
                    listing.save()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing row: {e}"))

        self.stdout.write(
            self.style.SUCCESS(f"Imported {Listing.objects.count()} listings.")
        )

        if options["reset"]:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Reset and imported {Listing.objects.count()} listings."
                )
            )
