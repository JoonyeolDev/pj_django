from django.urls import path
from . import views

urlpatterns = [
    path('product-list/', views.product_list, name='product-list'),
    path('product-create/', views.product_create, name='product-create'),
    path('inbound-create/<int:product_id>', views.inbound_create, name='inbound-create'),
    path('outbound-create/<int:product_id>', views.outbound_create, name='outbound-create'),
    path('inventory/<int:product_id>', views.inventory, name='inventory'),

]
