from django.core import exceptions
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets, status, mixins, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from gcm import GCM

from wl import models, serializers, custom_permissions

# class OwlUserMe(generics.RetrieveUpdateAPIView):
#     model = models.OwlUser
#     serializer_class = serializers.OwlUserSerializer
#     permission_classes  = (permissions.IsAuthenticated,)

#     def get_object(self):
#         return self.request.user

API_KEY = 'AIzaSyDAF3IRxpoDYLENrpEYhIHJwZ2w13QO07Q'

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,])
def replyJjokji(request):
    message = request.DATA.get('message')
    reg_id = request.DATA.get('reg_id')

    jjokji = request.user.jjokji_set.create(contents=message)

    gcm = GCM(API_KEY)
    data = {'reg_id': reg_id,
            'message': (jjokji.contents).encode('utf8')}
    gcm.plaintext_request(
        registration_id=request.user.gcmId, data=data
    )

    return Response(status=204)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,])
def sendJjokji(request):
    message = request.DATA.get('message')
    latitude = request.DATA.get('latitude')
    longitude = request.DATA.get('longitude')

    try:
        booeonglee = request.user.booeonglee_set.filter(
            houseofbooeonglee__purposeOfUse=0
        ).filter(houseofbooeonglee__state=0)[0]
    except:
        return Response(status=400)

    try:
        location = models.Location.objects.create(latitude=latitude,
                                                longitude=longitude,
                                                content_object=booeonglee)
    except:
        return Response(status=400)

    jjokji = request.user.jjokji_set.create(contents=message)

    booeonglee.jjokji = jjokji
    booeonglee.save()

    houseofbooeonglee = booeonglee.houseofbooeonglee
    houseofbooeonglee.state = 1
    houseofbooeonglee.save()

    contentType = ContentType.objects.get(name='owl user')
    locations = models.Location.objects.filter(content_type=contentType)

    for i in locations:
        if str('%.3f'%float(i.latitude)) == str('%.3f'%float(location.latitude)):
            if str('%.3f'%float(i.longitude)) == str('%.3f'%float(location.longitude)):
                data = {'reg_id': jjokji.writer.gcmId,
                        'message': (jjokji.contents).encode('utf8')}

                gcm = GCM(API_KEY)
                gcm.plaintext_request(
                    registration_id=i.content_object.gcmId, data=data
                )
                try:
                    booeonglee = i.content_object.booeonglee_set.filter(
                        houseofbooeonglee__purposeOfUse=1
                    ).filter(houseofbooeonglee__state=0)[0]
                except:
                    return Response(status=400)

                return Response(status=204)

    return Response(status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,])
def setLocation(request):
    latitude = request.DATA.get('latitude')
    longitude = request.DATA.get('longitude')

    try:
        models.Location.objects.create(latitude=latitude, longitude=longitude,
                                content_object=request.user)
    except:
        return Response(status=400)

    return Response(status=204)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated,])
def OwlUserMe(request):
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        serializer = serializers.OwlUserSerializer(request.user,
                                                    data=request.DATA,
                                                    files=request.FILES,
                                                    partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200,)
        return Response(serializer.errors, status=400)
    else:
        serializer = serializers.OwlUserSerializer(request.user)

        return Response(serializer.data, status=200,)

class OwlUserViewSet(viewsets.ModelViewSet):
    queryset = models.OwlUser.objects.all()
    serializer_class = serializers.OwlUserSerializer
    permission_classes = [custom_permissions.IsOwnerOrReadOnly]

    def post_save(self, obj, created=False):
        for i in xrange(3):
            booeonglee = obj.booeonglee_set.create()
            models.HouseOfBooeonglee.objects.create(purposeOfUse=0, state=0,
                                                    owner=booeonglee)

        for i in xrange(2):
            models.HouseOfBooeonglee.objects.create(purposeOfUse=1, state=0)

        return super(OwlUserViewSet, self).post_save(obj, created)

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
