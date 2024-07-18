from django.urls import path, include, re_path
from . import views
# from django.conf.urls import url
from ckeditor_uploader import views as ckeditor_views

urlpatterns = [
    path(r'^ckeditor/upload/', ckeditor_views.upload, name='ckeditor_upload'),
    path(r'^ckeditor/browse/', ckeditor_views.browse, name='ckeditor_browse'),
     path('change_status/<int:test_id>/<int:status>/', views.change_status, name='change_status'),
    path('change_status_legal/<int:test_id>/<int:status>/', views.change_status_legal, name='change_status_legal'),
    path('change_status_brand/<int:test_id>/<int:status>/', views.change_status_brand, name='change_status_brand'),
    path('', views.main_page, name='main_page'),
    path('check/', views.check, name='check'),
    path('pdf_model_stage/<str:model_name>/<str:test_stage>/',views.pdf_model_stage,name = 'pdf_model_stage'),
    path('legal_dashboard/',views.legal_dashboard,name = 'legal_dashboard'),
    path('brand_dashboard/',views.brand_dashboard,name = 'brand_dashboard'),
    path('dashboard/',views.dashboard,name = 'dashboard'),
    path('logout/',views.logout,name = 'logout'),
    path('submit-product-details', views.submit_product_details_view, name='submit_product_details'),
    path('edit/<str:test_name>/<str:model_name>/<str:serialno>/', views.edit, name='edit'),
    path('view/<str:test_name>/<str:model_name>/<str:serialno>/', views.view, name='view'),
    path('owner_view/<str:test_name>/<str:model_name>/<str:serialno>/', views.owner_view, name='owner_view'),
    path('legal_view/<str:test_name>/<str:model_name>/<str:serialno>/', views.legal_view, name='legal_view'),
    path('brand_view/<str:test_name>/<str:model_name>/<str:serialno>/', views.brand_view, name='brand_view'),
    path('cooling/<str:test_name>/<str:model_name>/<str:serialno>/', views.cooling, name='cooling'),
    path('mnf/', views.MNF, name='mnf'),
    path('test_list_entry/',views.Test_list_entry,name = 'test_list_entry'),
    path('update_test_list_entry/',views.update_test_list_entry,name = 'update_test_list_entry'),
    path('test_protocol_entry/<str:test_name>/<str:product>/',views.test_protocol_entry,name = 'test_protocol_entry'),
    path('set_status/<int:id>/', views.set_status, name='set_status'),
    path('delete-test-record/<int:record_id>/', views.delete_test_record, name='delete_test_record'),
    path('remark/<int:id>/',views.remark,name = 'remark'),
    path('remark_owner/<int:id>/',views.owner_remark,name = 'remark_owner'),
    path('view_pdf/<str:test_name>/<str:model_name>/<str:serialno>/', views.view_pdf, name='view_pdf'),
    path('handle_selected_tests/',views.handle_selected_tests,name = 'handle_selected_tests'),
    path('base/',views.base,name = 'base'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)