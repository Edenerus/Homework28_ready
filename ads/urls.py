from django.urls import path

from ads.views import ads, cat

urlpatterns = [
    path('', ads.AdListView.as_view()),
    path('<int:pk>/', ads.AdDetailView.as_view()),
    path('create/', ads.AdCreateView.as_view()),
    path('<int:pk>/update/', ads.AdUpdateView.as_view()),
    path('<int:pk>/delete/', ads.AdDeleteView.as_view()),
    path('<int:pk>/image/', ads.AdImageView.as_view()),
    path('cat/', cat.CatListView.as_view()),
    path('cat/create/', cat.CatCreateView.as_view()),
    path('cat/<int:pk>/', cat.CatDetailView.as_view()),
    path('cat/<int:pk>/delete/', cat.CatDeleteView.as_view()),
    path('by_user/', ads.AuthorAdDetailView.as_view())
]
