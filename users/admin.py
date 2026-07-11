# Import Django admin panel
from django.contrib import admin

# Import our custom User model
from .models import User

# Register User model in Django admin
admin.site.register(User)