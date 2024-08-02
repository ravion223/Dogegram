from django.urls import path
from .views import IndexView, search_view
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(IndexView.as_view()), name='main-page'),
    path('search/', search_view, name='search')
]

app_name = 'main_page'