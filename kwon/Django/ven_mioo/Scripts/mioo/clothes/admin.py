from django.contrib import admin # userid : admin

# Register your models here.
from .models import clothes

admin.site.register(clothes)