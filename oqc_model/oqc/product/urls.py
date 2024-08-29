from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_form_view, name='product'),
    path('AC/', views.AC_spec, name='AC'),
    path('TestNames/', views.TestNames, name='TestNames'),
    path('WM-FATL/', views.WM_FATL_spec, name='WM-FATL'),
]