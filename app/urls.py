from django.urls import path
from .views import ContactAPI, ContactAPIUpdateDelete,ContactSearchAPI

app_name = 'api'
urlpatterns = [
    path('', ContactAPI.as_view(), name='contact'),
    path('<str:custom_id>', ContactAPIUpdateDelete.as_view(), name='update and delete view'),
    path('search/<str:full_name>/', ContactSearchAPI.as_view(), name='search'),
]
