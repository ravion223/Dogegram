from django.urls import path
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='main-page'),
]

app_name = 'main_page'