from django.contrib import admin
from .models import CustomUser, Contact

admin.site.register(CustomUser)
admin.site.register( Contact)