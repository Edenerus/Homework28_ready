import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, DeleteView, ListView, CreateView
from django.core.paginator import Paginator

from ads.models import Category
from avito.settings import TOTAL_ON_PAGE


@method_decorator(csrf_exempt, name='dispatch')
class CatListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        categories = []
        for cat in page_obj:
            categories.append({
                "id": cat.id,
                "name": cat.name,
            })

        response = {
            "items": categories,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CatCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"],
        )

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class CatDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
