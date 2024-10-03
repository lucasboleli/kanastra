from django.urls import path

from charge.views import ChargeViewSet

urlpatterns = [
    path(
        "create-charge/",
        ChargeViewSet.as_view({"post": "create"}),
        name="create-charge",
    ),
]
