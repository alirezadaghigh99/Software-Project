from django.urls import path

from home.views import home_page

app_name = 'home'
urlpatterns = [
    path('', home_page, name='home'),
]
