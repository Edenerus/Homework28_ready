import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Avg, Count

from ads.models import Ad
from users.models import User
from avito.settings import TOTAL_ON_PAGE


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related("author").order_by("price")

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

#       total = self.object_list.count()
#       page_number = int(request.GET.get("page", 1))
#       offset = (page_number - 1) * settings.TOTAL_ON_PAGE
#       if offset < total:
#           self.object_list = self.object_list[offset:offset+settings.TOTAL_ON_PAGE]
#       else:
#           self.object_list = self.object_list[offset:offset+total]

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": ad.image.url,
                "category": ad.category_id,
                "author": ad.author_id,
            })

        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image.url,
            "category": ad.category_id,
            "author": ad.author_id,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "price", "description", "is_published", "image", "category", "author"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ad = Ad.objects.create(
            name=ad_data["name"],
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            category_id=ad_data["category_id"] if ad_data["category_id"] else None
        )

        ad.author = get_object_or_404(User, pk=ad_data["author_id"])

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "price": ad.price,
            "description": ad.description,
            "image": ad.image.url if ad.image else None,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "author_id": ad.author_id,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "image": self.object.image.url if self.object.image else None
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "price", "description", "image", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        self.object.name = ad_data["name"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.category_id = ad_data["category_id"]

        self.object.save()

        return JsonResponse({
            "name": self.object.name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "author_id": self.object.author_id,
            "image": self.object.image.url if self.object.image else None
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class AuthorAdDetailView(View):
    def get(self, request):
        author_qs = User.objects.annotate(ads=Count('ad'))

        paginator = Paginator(author_qs, TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        authors = []
        for author in page_obj:
            authors.append({
                "id": author.id,
                "username": author.username,
                "ads": author.ads
            })

        response = {
            "items": authors,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "avg": author_qs.aggregate(avg=Avg('ads'))['avg']
        }

        return JsonResponse(response)
