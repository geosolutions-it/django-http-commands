from django.urls import re_path
from .views import ManagementCommandView


urlpatterns = [
    re_path(r'management/$', ManagementCommandView.as_view()),
    re_path(r'management/(?P<cmd>\w+)/$', ManagementCommandView.as_view()),
]
