from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = i18n_patterns(
    path("polls/", include("polls.urls")),
    path("contact/", include("contact.urls")),
    path("blog/", include("blog.urls")),
    path("admin/", admin.site.urls),
    path("subscriptions/", include("subscriptions.urls")),
    path("accounts/", include("accounts.urls")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
