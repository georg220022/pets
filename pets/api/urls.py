from django.urls import path, include
from .views import PetsModelViewSet

urlpatterns = [
    path(
        "pets",
        PetsModelViewSet.as_view({"get": "list", "post": "create", "delete": "delete"}),
    ),
    path("pets/<id>/photo", PetsModelViewSet.as_view({"post": "add_photo"})),
]
