from django.urls import path
from . import views

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
]
