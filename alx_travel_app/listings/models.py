from django.db import models

# Create your models here.


class Status(models.TextChoices):
    pending = "pending", "Pending"
    confirmed = "confirmed", "Confirmed"
    cancelled = "cancelled", "Cancelled"


class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    num_bedrooms = models.IntegerField()
    num_bathrooms = models.IntegerField()
    max_guests = models.IntegerField()
    amenities = models.TextField(
        blank=True, null=True
    )  # JSON or comma-separated values
    owner_id = models.ForeignKey(
        "auth.User",  # Assuming you have a User model in auth app
        on_delete=models.CASCADE,
        related_name="listings",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.CharField(
        max_length=100
    )  # Assuming a simple string for user, can be replaced with a User model
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.pending,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking for {self.listing.title} by {self.user}"


class Review(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.CharField(
        max_length=100
    )  # Assuming a simple string for user, can be replaced with a User model
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Review for {self.listing.title} by {self.user}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    booking_ref = models.CharField(max_length=100, unique=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.booking_ref} - {self.status}"
