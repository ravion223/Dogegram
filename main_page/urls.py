from django.urls import path
from .views import IndexView, search_view

urlpatterns = [
    path('', IndexView.as_view(), name='main-page'),
    path('search/', search_view, name='search')
]

app_name = 'main_page'