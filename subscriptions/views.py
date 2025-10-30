import stripe
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .models import Subscription, Order


def index(request):
    return render(
        request,
        "subscriptions/index.html",
        {"subscriptions": Subscription.objects.all()},
    )


def create_checkout_session(request, sub_id):
    sub = get_object_or_404(Subscription, pk=sub_id)
    order = Order(subscription=sub)
    order.save()
    checkout_session = stripe.checkout.Session.create(
        client_reference_id=order.id,
        # Schema: https://docs.stripe.com/api/checkout/sessions/create#create_checkout_session-line_items
        line_items=[
            {
                "price_data":
                # Schema: https://docs.stripe.com/api/products/create
                {
                    "unit_amount": sub.price,  # must be in cents
                    "currency": "cad",
                    "product_data": {
                        "name": sub.name,
                        "images": [
                            "https://www.pngall.com/wp-content/uploads/14/Subscribe-Button-No-Background.png"
                        ],
                    },
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("subscriptions:success"),
        ),
        cancel_url=request.build_absolute_uri(
            reverse("subscriptions:cancel"),
        ),
    )
    return redirect(checkout_session.url, code=303)


def success(request):
    return render(request, "subscriptions/success.html")


def cancel(request):
    return render(request, "subscriptions/cancel.html")
