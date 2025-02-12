from django.contrib import admin
from finances.models import Category, Transaction

admin.site.register(Category)
admin.site.register(Transaction)