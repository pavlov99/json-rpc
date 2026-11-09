try:
    from django.conf.urls import url, include  # Django<4.0
except ImportError:
    from django.urls import re_path as url, include  # Django>=4.0
from jsonrpc.backend.django import api

urlpatterns = [
    url(r'', include(api.urls)),
    url(r'^prefix/', include(api.urls)),
]
