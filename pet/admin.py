from django.contrib import admin
from pet.models import Pet, Review, Category

# Register your models here.

admin.site.register(Pet)
admin.site.register(Review)
admin.site.register(Category)
