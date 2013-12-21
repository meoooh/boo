from django.conf.urls import patterns, include, url

from rest_framework import routers

from wl import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', views.OwlUserViewSet)

urlpatterns = patterns('wl',
	# url(r'^users/?$', views.OwlUserCreateRetrieve),
	url(r'^users/is-exist/?$', views.isExist),
	# url(r'^users/(?P<pk>\d+)/?$', views.OwlUserCreateRetrieve),
	url(r'', include(router.urls)),
	url(r'', include('gcm.urls')),
	url(r'^me/?$', views.OwlUserMe)
)
