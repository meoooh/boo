from django.conf.urls import patterns, include, url

from rest_framework import routers

from wl import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', views.OwlUserViewSet)

urlpatterns = patterns('wl',
	url(r'^', include(router.urls)),
)
