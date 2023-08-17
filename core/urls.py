from django.contrib import admin
from django.urls import path,include,re_path
from django.views.static import serve 
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/",include("accounts.urls")),
    path("api/", include('travel.urls')),
    path('', include('admin_volt.urls')),
    path('openapi', get_schema_view(
        title="My Trip My Ticket",
        description="",
        version="1.0.0"
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='docs'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
