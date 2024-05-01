from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser,CodesVerification

# Register your models here.
class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ('id', "first_name", "last_name", "email","user_type", "date_joined")
    fieldsets = (
      ('Employee info', {
          'fields': ('username','email','password','first_name','last_name','user_type','is_staff')
      }),
   )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CodesVerification)
admin.site.unregister(Group)