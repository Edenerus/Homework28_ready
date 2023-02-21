from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet

from ads.models import Categorie
from ads.serializers import CategorieSerializer


def index(request):
    response = {"status": "ok"}
    return JsonResponse(response, safe=False)


class CatViewSet(ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
