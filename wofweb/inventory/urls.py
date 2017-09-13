from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='Index'),
    url(r'^items/$', views.Items.as_view(), name='Items'),
]
