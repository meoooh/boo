from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

from wl import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', views.OwlUserViewSet)

urlpatterns = patterns('wl',
	# url(r'^users/?$', views.OwlUserCreateRetrieve),
	url(r'^users/is-exist/?$', views.isExist),
	# url(r'^users/(?P<pk>\d+)/?$', views.OwlUserCreateRetrieve),
	url(r'', include(router.urls)),
	url(r'^me/?$', views.OwlUserMe),
	url(r'^set-current-location/?$', views.setLocation),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
