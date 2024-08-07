from django.urls import path
from . import views

urlpatterns = [
    path('product/',views.product_form_view,name = 'product'),
    path('AC/',views.AC_spec,name = 'AC'),
]