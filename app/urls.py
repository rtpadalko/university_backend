from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('specializations/<int:specialization_id>/', specialization),
    path('orders/<int:order_id>/', order),
]