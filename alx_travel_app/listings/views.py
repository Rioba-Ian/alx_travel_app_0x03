from rest_framework import viewsets
from .models import Listing, Booking, Payment
import uuid
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.conf import settings
import requests
from django.db import models

# Create your views here.
from .serializers import ListingSerializer, BookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class InitiatePaymentView(View):
    def post(self, request, *args, **kwargs):
        # Logic to initiate payment
        data = request.data
        amount = data.get("amount")
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        booking_ref = str(uuid.uuid4())

        payment = Payment.objects.create(
            booking_ref=booking_ref,
            transaction_id=str(uuid.uuid4()),
            amount=amount,
            currency="USD",
            status="pending",
        )

        payload = {
            "amount": amount,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "tx_ref": booking_ref,
            "callback_url": "https://your-callback-url.com/payment/callback",
            "return_url": "https://your-return-url.com/payment/return",
            "customization[title]": "Payment for Booking",
            "customization[description]": f"Payment for booking reference {booking_ref}",
        }

        headers = {
            "Authorization": f"Beaerer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{settings.CHAPA_BASE_URL}/transaction/initialize",
            json=payload,
            headers=headers,
        )

        resp_json = response.json()
        if resp_json.get("status") == "success":
            payment.transaction_id = booking_reference
            payment.save()
            return JsonResponse({"payment_url": resp_json["data"]["checkout_url"]})
        else:
            payment.status = "Failed"
            payment.save()
            return JsonResponse({"error": "Payment initiation failed"}, status=400)


class VerifyPaymentView(View):
    def get(self, request, *args, **kwargs):
        # Logic to verify payment
        tx_ref = request.GET.get("tx_ref")
        try:
            payment = Payment.objects.get(booking_ref=tx_ref)
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)

        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}

        response = requests.get(
            f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}", headers=headers
        )
        resp_json = response.json()

        if (
            resp_json.get("status") == "success"
            and resp_json["data"]["status"] == "success"
        ):
            payment.status = "Completed"
            payment.save()
            #  Trigger Celery email notification
            return JsonResponse({"message": "Payment successful"})
        else:
            payment.status = "Failed"
            payment.save()
            return JsonResponse({"message": "Payment failed"}, status=400)
