import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, DeleteView, ListView, CreateView
from django.core.paginator import Paginator

from users.models import Location
from avito.settings import TOTAL_ON_PAGE


@method_decorator(csrf_exempt, name='dispatch')
class LocationListView(ListView):
    model = Location

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        locations = []
        for location in page_obj:
            locations.append({
                "id": location.id,
                "name": location.name,
                "lat": location.lat,
                "lng": location.lng
            })

        response = {
            "items": locations,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class LocationCreateView(CreateView):
    model = Location
    fields = ["name", "lat", "lng"]

    def post(self, request, *args, **kwargs):
        location_data = json.loads(request.body)

        location = Location.objects.create(
            name=location_data["name"],
            lat=location_data["lat"],
            lng=location_data["lng"],
        )

        return JsonResponse({
            "id": location.id,
            "name": location.name,
            "lat": location.lat,
            "lng": location.lng
        })


class LocationDetailView(DetailView):
    model = Location

    def get(self, request, *args, **kwargs):
        location = self.get_object()

        return JsonResponse({
            "id": location.id,
            "name": location.name,
            "lat": location.lat,
            "lng": location.lng
        })


@method_decorator(csrf_exempt, name="dispatch")
class LocationDeleteView(DeleteView):
    model = Location
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
