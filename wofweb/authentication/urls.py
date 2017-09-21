from django.conf.urls import include, url


from rest_framework import routers


from . import views


router = routers.SimpleRouter()
router.register(r'accounts', views.AccountViewSet)


urlpatterns = [
    url(r'^api/v1/', views.AccountViewSet.as_view(), name='register')
]
