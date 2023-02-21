from rest_framework.viewsets import ModelViewSet

from users.models import Location
from users.serializers import LocationSerializer


class LocViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
