from django.urls import path
from . import views
app_name = "products"
urlpatterns = [
    path("", views.product_list, name="list"),
    path("add/", views.product_add, name="add"),
    path("<int:pk>/label/", views.product_label, name="label"),
]
