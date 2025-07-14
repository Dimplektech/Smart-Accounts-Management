import stripe
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from .models import Payment, Subscription, PremiumFeature
from decimal import Decimal
from django.contrib.auth.models import User


def user_has_premium(user):
    """Check if user has premium access"""
    return Payment.objects.filter(
        user=user, status="completed", payment_type="premium_upgrade"
    ).exists()


@login_required
def pricing_page(request):
    """Display simple pricing plans"""
    plans = [
        {
            "name": "Free",
            "price": 0,
            "features": [
                "Basic Receipt Scanning",
                "Up to 10 receipts/month",
                "Basic expense tracking",
            ],
            "is_free": True,
        },
        {
            "name": "Premium",
            "price": 9.99,
            "features": [
                "Unlimited Receipt Scanning",
                "Advanced OCR Processing",
                "Expense Analytics",
                "Data Export",
                "Priority Support",
            ],
            "is_free": False,
        },
    ]
    return render(
        request,
        "payments/simple_pricing.html",
        {"plans": plans, "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY},
    )


@login_required
def create_payment_intent(request):
    """Create a Stripe Payment Intent"""
    if request.method == "POST":
        try:
            # Set Stripe API key
            stripe.api_key = settings.STRIPE_SECRET_KEY

            data = json.loads(request.body)
            amount = int(float(data.get("amount", 0)) * 100)  # Convert to cents
            payment_type = data.get("payment_type", "premium_upgrade")

            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                metadata={"user_id": request.user.id, "payment_type": payment_type},
            )

            # Create payment record
            payment = Payment.objects.create(
                user=request.user,
                stripe_payment_intent_id=intent.id,
                amount=Decimal(amount / 100),
                payment_type=payment_type,
                description=data.get("description", ""),
            )

            return JsonResponse(
                {"client_secret": intent.client_secret, "payment_id": payment.id}
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def payment_success(request):
    """Handle successful payment"""
    payment_intent_id = request.GET.get("payment_intent")

    if payment_intent_id:
        try:
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
            payment.status = "completed"
            payment.save()

            # If it's a premium upgrade, no need for additional features
            # The payment record itself indicates premium access

            messages.success(
                request, "Payment completed successfully! You now have premium access!"
            )

        except Payment.DoesNotExist:
            messages.error(request, "Payment not found.")

    return render(request, "payments/success.html")


@login_required
def payment_cancel(request):
    """Handle cancelled payment"""
    messages.info(request, "Payment was cancelled.")
    return render(request, "payments/cancel.html")


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    # Set Stripe API key
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the event
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]

        try:
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent["id"])
            payment.status = "completed"
            payment.save()
        except Payment.DoesNotExist:
            pass

    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]

        try:
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent["id"])
            payment.status = "failed"
            payment.save()
        except Payment.DoesNotExist:
            pass

    return HttpResponse(status=200)


@login_required
def premium_features(request):
    """Display simple premium upgrade"""
    # Check if user already has premium
    has_premium = Payment.objects.filter(
        user=request.user, status="completed", payment_type="premium_upgrade"
    ).exists()

    upgrade_info = {
        "name": "Premium Upgrade",
        "price": 9.99,
        "description": "Unlock all premium features for lifetime access",
        "features": [
            "Unlimited Receipt Scanning",
            "Advanced OCR Processing",
            "Expense Analytics Dashboard",
            "Export Data (PDF, Excel)",
            "Priority Support",
        ],
        "has_premium": has_premium,
    }

    return render(
        request,
        "payments/simple_premium.html",
        {
            "upgrade": upgrade_info,
            "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        },
    )


@login_required
def payment_history(request):
    """Display user's payment history"""
    payments = Payment.objects.filter(user=request.user)
    return render(request, "payments/history.html", {"payments": payments})
