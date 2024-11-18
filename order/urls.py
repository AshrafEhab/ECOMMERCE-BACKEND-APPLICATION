from django.urls import path
from . import views
urlpatterns = [
    path('orders/',views.get_all_orders,name='get_all_orders' ),
    path('orders/new/',views.new_order,name='new_order' ),
    path('orders/<str:pk>/',views.get_order_by_id,name='get_order_by_id' ),
    path('orders/delete/<str:pk>/',views.delete_order_by_id,name='delete_order_by_id' ),
    path('orders/edit/<str:pk>/',views.edit_order_status_by_id,name='edit_order_status_by_id' ),
]
