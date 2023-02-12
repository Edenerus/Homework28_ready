from django.urls import path

from users.views import user, location

urlpatterns = [
    path('', user.UserListView.as_view()),
    path('<int:pk>/', user.UserDetailView.as_view()),
    path('create/', user.UserCreateView.as_view()),
    path('<int:pk>/update/', user.UserUpdateView.as_view()),
    path('<int:pk>/delete/', user.UserDeleteView.as_view()),
    path('loc/', location.LocationListView.as_view()),
    path('loc/create/', location.LocationCreateView.as_view()),
    path('loc/<int:pk>/', location.LocationDetailView.as_view()),
    path('loc/<int:pk>/delete/', location.LocationDeleteView.as_view()),
]
