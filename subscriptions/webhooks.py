import os

import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import Order


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe events.

    Stripe Event object schema: https://docs.stripe.com/api/events/object
    """
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ["STRIPE_WEBHOOK_SECRET"]
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if (
        event["type"] == "checkout.session.completed"
        or event["type"] == "checkout.session.async_payment_succeeded"
    ):
        stripe_session = event["data"]["object"]
        order_id = stripe_session["client_reference_id"]
        order = Order.objects.get(id=order_id)
        customer_details = stripe_session["customer_details"]
        order.fulfill(
            name=customer_details["name"],
            email=customer_details["email"],
            payment_id=stripe_session["payment_intent"],
        )

    return HttpResponse(status=200)
