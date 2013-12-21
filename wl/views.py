from django.core import exceptions

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from wl import models, serializers

class OwlUserViewSet(viewsets.ModelViewSet):
    queryset = models.OwlUser.objects.all()
    serializer_class = serializers.OwlUserSerializer

@api_view(['GET'])
def isExist(request):
    deviceId = request.GET.get('q')

    try:
        models.OwlUser.objects.get(deviceId=deviceId)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)