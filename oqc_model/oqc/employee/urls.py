from django.urls import path, include, re_path
from . import views
from ckeditor_uploader import views as ckeditor_views
from django.views.static import serve
from django.conf import settings

handler404 = 'employee.views.custom_404'

urlpatterns = [
    path(r'^ckeditor/upload/', ckeditor_views.upload, name='ckeditor_upload'),
    path(r'^ckeditor/browse/', ckeditor_views.browse, name='ckeditor_browse'),
    path('change_status/<int:test_id>/<int:status>/', views.change_status, name='change_status'),
    path('change_status_legal/<int:test_id>/<int:status>/', views.change_status_legal, name='change_status_legal'),
    path('change_status_brand/<int:test_id>/<int:status>/', views.change_status_brand, name='change_status_brand'),
    path('', views.main_page, name='main_page'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('legal_dashboard/', views.legal_dashboard, name='legal_dashboard'),
    path('brand_dashboard/', views.brand_dashboard, name='brand_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('edit/<str:stage>/<str:product>/<str:test_name>/<str:model_name>/<str:serialno>/', views.edit, name='edit'),
    path('view/<str:stage>/<str:product>/<str:test_name>/<str:model_name>/<str:serialno>/', views.view, name='view'),
    path('owner_view/<str:stage>/<str:product>/<str:test_name>/<str:model_name>/<str:serialno>/', views.owner_view, name='owner_view'),
    path('legal_view/<str:stage>/<str:product>/<str:test_name>/<str:model_name>/<str:serialno>/', views.legal_view, name='legal_view'),
    path('brand_view/<str:stage>/<str:product>/<str:test_name>/<str:model_name>/<str:serialno>/', views.brand_view, name='brand_view'),
    path('report/<str:stage>/<str:product>/<str:test_name>/<str:model_name>/<str:serialno>/', views.report, name='report'),
    path('mnf/', views.MNF, name='mnf'),
    path('model_details_update/', views.model_details_update, name='model_details_update'),
    path('model_details_view/', views.model_details_view, name='model_details_view'),
    path('test_list_entry/', views.Test_list_entry, name='test_list_entry'),
    path('update_test_list_entry/', views.update_test_list_entry, name='update_test_list_entry'),
    path('test_details_view/', views.test_details_view, name='test_details_view'),
    path('test_protocol_entry/<str:test_name>/<str:product>/', views.test_protocol_entry, name='test_protocol_entry'),
    path('set_status/<int:id>/', views.set_status, name='set_status'),
    path('delete-test-record/<int:record_id>/', views.delete_test_record, name='delete_test_record'),
    path('view_pdf/<str:stage>/<str:product>/<str:test_name>/<str:model_name>/<str:serialno>/', views.view_pdf, name='view_pdf'),
    path('handle_selected_tests/<str:product>/<str:model>/<str:action>/', views.handle_selected_tests, name='handle_selected_tests'),
    path('access_denied/', views.access_denied, name='access_denied'),
	path('ckeditor_image_upload/', views.ckeditor_image_upload, name='ckeditor_image_upload'),
    path('server_media_browse/', views.server_media_browse, name='server_media_browse'),
    path('handle_notification/', views.handle_notification, name='handle_notification'),
    path('clear_notification/', views.clear_notification, name='clear_notification'),
    path('notifications/', views.notifications, name='notifications'),
    path('to_dashboards/', views.to_dashboards, name='to_dashboards'),
    path('mark_all_as_read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('delete_notification/', views.delete_notification, name='delete_notification'),
    path('make_remark_changes/', views.make_remark_changes, name='make_remark_changes'),
    path('delete_remark/', views.delete_remark, name='delete_remark'),
    path('reply_remark/', views.reply_remark, name='reply_remark'),
    re_path(r'^user_manual\.pdf$', serve, {'document_root': settings.STATICFILES_DIRS[0], 'path': 'documents/user_manual.pdf'}),
    path('weekly_update/', views.weekly_update, name='weekly_update'),
    path('add_tracker_model/', views.add_tracker_model, name='add_tracker_model'),
    path('update_cell/', views.update_cell, name='update_cell'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)