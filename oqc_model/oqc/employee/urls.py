from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('members/', views.members, name='members'),  
    path('testdetail/<int:no>/', views.testdetail, name='testdetail'),
    path('check/', views.check, name='check'),
    path('dashboard/',views.dashboard,name = 'dashboard'),
    path('logout/',views.logout,name = 'logout'),
    path('submit-product-details', views.submit_product_details_view, name='submit_product_details'),
    path('create-test-record/', views.create_test_record, name='create_test_record'),
    path('edit-test-record/<int:pk>/', views.edit_test_record, name='edit_test_record'),
    path('view/', views.view_test_records, name='view'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('view_test_report/<int:pk>/', views.view_test_report, name='view_test_reports'),
    path('cooling/<str:test_name>/<str:model_name>/', views.cooling, name='cooling'),
    path('mnf/', views.MNF, name='mnf'),
    path('test_list_entry/',views.Test_list_entry,name = 'test_list_entry'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)