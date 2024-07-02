from django.urls import path, include, re_path
from . import views
# from django.conf.urls import url
from ckeditor_uploader import views as ckeditor_views

urlpatterns = [
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path(r'^ckeditor/upload/', ckeditor_views.upload, name='ckeditor_upload'),
    path(r'^ckeditor/browse/', ckeditor_views.browse, name='ckeditor_browse'),
    path('', views.main_page, name='main_page'),
    # path('members/', views.members, name='members'),  
    # path('testdetail/<int:no>/', views.testdetail, name='testdetail'),
    path('check/', views.check, name='check'),
    path('dashboard/',views.dashboard,name = 'dashboard'),
    path('logout/',views.logout,name = 'logout'),
    path('submit-product-details', views.submit_product_details_view, name='submit_product_details'),
    # path('create-test-record/', views.create_test_record, name='create_test_record'),
    # path('edit-test-record/<int:pk>/', views.edit_test_record, name='edit_test_record'),
    path('edit/<str:test_name>/<str:model_name>/<str:serialno>/', views.edit, name='edit'),
    path('view/<str:test_name>/<str:model_name>/<str:serialno>/', views.view, name='view'),
    path('owner_view/<str:test_name>/<str:model_name>/<str:serialno>/', views.owner_view, name='owner_view'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    # path('view_test_report/<int:pk>/', views.view_test_report, name='view_test_reports'),
    path('cooling/<str:test_name>/<str:model_name>/<str:serialno>/', views.cooling, name='cooling'),
    path('mnf/', views.MNF, name='mnf'),
    path('test_list_entry/',views.Test_list_entry,name = 'test_list_entry'),
    path('test_protocol_entry/',views.test_protocol_entry,name = 'test_protocol_entry'),
    path('toggle_status/<int:id>/', views.toggle_status, name='toggle_status'),
    path('set_status/<int:id>/', views.set_status, name='set_status'),
    path('delete-test-record/<int:record_id>/', views.delete_test_record, name='delete_test_record'),
    path('remark/<int:id>/',views.remark,name = 'remark'),
    path('remark_owner/<int:id>/',views.owner_remark,name = 'remark_owner'),
    path('send_report/<int:report_id>/', views.send_report, name='send_report'),
    path('view_pdf/<str:test_name>/<str:model_name>/<str:serialno>/', views.view_pdf, name='view_pdf'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)