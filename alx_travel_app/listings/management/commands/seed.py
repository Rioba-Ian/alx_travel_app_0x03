from datetime import datetime
from django.core.management.base import BaseCommand
from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        # Create sample listings
        listings = [
            Listing(
                title="Cozy Cottage",
                description="A cozy cottage in the countryside.",
                address="123 Country Lane",
                city="Countryside",
                state="CA",
                country="USA",
                price_per_night=100.00,
                num_bedrooms=2,
                num_bathrooms=1,
                max_guests=4,
                amenities="WiFi, Kitchen, Parking",
                owner_id=None,  # Replace with actual user instance
                price=100.00,
                available=True,
            ),
            Listing(
                title="Beachfront Villa",
                description="A luxurious villa by the beach.",
                address="456 Ocean Drive",
                city="Beach City",
                state="FL",
                country="USA",
                price_per_night=300.00,
                num_bedrooms=3,
                num_bathrooms=2,
                max_guests=6,
                amenities="Pool, WiFi, Air Conditioning",
                owner_id=None,  # Replace with actual user instance
                price=300.00,
                available=True,
            ),
        ]

        Listing.objects.bulk_create(listings)

        # Create sample bookings
        bookings = [
            Booking(
                listing_id=listings[0],
                user="john_doe",
                check_in_date=datetime(2023, 10, 1),
                check_out_date=datetime(2023, 10, 5),
                num_guests=2,
                status="confirmed",
            ),
            Booking(
                listing_id=listings[1],
                user="jane_doe",
                check_in_date=datetime(2023, 11, 1),
                check_out_date=datetime(2023, 11, 7),
                num_guests=4,
                status="pending",
            ),
        ]

        Booking.objects.bulk_create(bookings)

        # Create sample reviews
        reviews = [
            Review(
                listing_id=listings[0],
                booking_id=bookings[0],
                user="john_doe",
                rating=5,
                comment="Great stay! Highly recommend.",
            ),
            Review(
                listing_id=listings[1],
                booking_id=bookings[1],
                user="jane_doe",
                rating=4,
                comment="Beautiful villa, but a bit pricey.",
            ),
        ]
        Review.objects.bulk_create(reviews)
