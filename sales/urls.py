from django.urls import path
from . import views
app_name = "sales"
urlpatterns = [
    path("", views.pos, name="pos"),
    path("api/scan/", views.scan_product, name="scan"),
    path("checkout/", views.checkout, name="checkout"),
    path("receipt/<int:pk>/", views.receipt, name="receipt"),
]
