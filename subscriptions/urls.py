from django.urls import path
from . import views, webhooks

app_name = "subscriptions"
urlpatterns = [
    path(
        "",
        views.index,
        name="index",
    ),
    path(
        "<int:sub_id>/create-checkout-session/",
        views.create_checkout_session,
        name="create_checkout_session",
    ),
    path(
        "success/",
        views.success,
        name="success",
    ),
    path(
        "cancel/",
        views.cancel,
        name="cancel",
    ),
    path(
        "webhook/",
        webhooks.stripe_webhook,
        name="fulfill_stripe_checkout_webhook",
    ),
]
