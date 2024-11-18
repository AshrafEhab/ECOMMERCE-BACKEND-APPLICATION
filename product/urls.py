from django.urls import path
from . import views
urlpatterns = [
    path('products/',views.get_all_products,name='products' ),
    path('products/<str:pk>',views.get_product,name='get_product' ),
    path('products/edit/<str:pk>',views.edit_product,name='edit_product' ),
    path('products/delete/<str:pk>',views.delete_product,name='delete_product' ),
    path('products/add/',views.add_product,name='get_product' ),

    path('<str:pk>/reviews/',views.add_review,name='add_review'),
    path('<str:pk>/reviews/delete/',views.delete_review,name='delete_review'),
    

]
