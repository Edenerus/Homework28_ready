import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from users.models import User, Location
from avito.settings import TOTAL_ON_PAGE


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("username")

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

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "location": list(map(str, user.location.all())),
            })

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "age": user.age,
            "location": map(str, user.location.all()),
        })


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
            age=user_data["age"],
        )

        if user_data["location"]:
            loc_obj, created = Location.objects.get_or_create(
                name=user_data["location"],
                defaults={
                    "is_active": True
                }
            )
            user.location.add(loc_obj)

        user.save()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "age": user.age,
            "location": list(map(str, user.location.all()))
        })


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "age", "location"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.age = user_data["age"]

        if user_data["location"]:
            loc_obj, created = Location.objects.get_or_create(
                name=user_data["location"],
                defaults={
                    "is_active": True
                }
            )
            self.object.location.add(loc_obj)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "age": self.object.age,
            "location_id": list(map(str, self.object.location.all()))
        })


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
