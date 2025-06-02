from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('soeid',)  # Display the SOEID field in the admin list view
    search_fields = ('soeid',)  # Enable search by SOEID
