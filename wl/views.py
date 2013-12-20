from rest_framework import generics, permissions, viewsets, mixins

from wl import models, serializers

class OwlUserViewSet(viewsets.ModelViewSet):
    queryset = models.OwlUser.objects.all()
    serializer_class = serializers.OwlUserSerializer