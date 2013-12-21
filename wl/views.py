from django.core import exceptions
from django.utils.translation import ugettext as _

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, action

from wl import models, serializers, custom_permissions

class OwlUserViewSet(viewsets.ModelViewSet):
    queryset = models.OwlUser.objects.all()
    serializer_class = serializers.OwlUserSerializer
    permission_classes = [custom_permissions.IsOwnerOrReadOnly]

    def list(self, request, *arg, **kwarg):
        return Response({'detail': "Method 'GET' not allowed."})

    def retrieve(self, request, *arg, **kwarg):
        user = self.get_object()

        if request.user == user:
            return super(OwlUserViewSet, self).retrieve(request, *arg, **kwarg)
        return Response(
            {
                'detail': _('Authentication credentials were not provided.')
            }
        )

    # def partial_update(self, request, *arg, **kwarg):
    #     super(OwlUserViewSet, self).partial_update(request, *arg, **kwarg)

    #     user = self.get_object()
    #     import ipdb; ipdb.set_trace()
    #     maxAge = request.DATA.get('max')
    #     minAge = request.DATA.get('min')

    #     serializer = serializers.OwlUserSerializer(user, 
    #                                             data={
    #                                                 'ideaTypeAgeMax': maxAge,
    #                                                 'ideaTypeAgeMin': minAge,
    #                                             },
    #                                             partial=True
    #     )
    #     # import ipdb; ipdb.set_trace()
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors, status=400)

@api_view(['GET'])
def isExist(request):
    deviceId = request.GET.get('q')

    try:
        models.OwlUser.objects.get(deviceId=deviceId)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)
