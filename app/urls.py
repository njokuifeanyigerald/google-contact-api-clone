from django.urls import path
from .views import ContactAPI, ContactAPIUpdate

app_name = 'api'
urlpatterns = [
    path('', ContactAPI.as_view(), name='contact'),
    path('<str:custom_id>', ContactAPIUpdate.as_view(), name='update and delete view'),
    # path('', ContactAPI.as_view(), name='contact'),
]
