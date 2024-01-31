from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ["id","email","username","ph","is_admin"]
    list_filter = ["is_admin"]

    def has_change_permission(self, request, obj=None):
        if obj is not None and request.user.is_staff_member and request.user != obj:
            return False
        return super().has_change_permission(request, obj)
    
    def get_fieldsets(self, request, obj=None):
        if obj:
            if request.user.is_admin:
                return (
                    ("User Credentials", {"fields": ["email", "password"]}),
                    ("Personal info", {"fields": ["username", "ph","address"]}),
                    ("Permissions", {"fields": ['is_superuser','is_admin','is_active','is_staff_member','is_merchant','groups','user_permissions']}),
                    ("Token_Verify", {"fields": ["tc"]}),
                )
            elif request.user.is_staff_member:
                return (
                    ("User Credentials", {"fields": ["email", "password"]}),
                    ("Personal info", {"fields": ["username", "ph","address"]}),
                    ("Token_Verify", {"fields": ["tc"]}),
              )
      
    
        return super().get_fieldsets(request, obj)
    
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_admin:
            self.add_fieldsets[0][1]['fields'] = ['email','password1','password2','username','ph','address','is_superuser','is_admin','is_active','is_staff_member','is_merchant','groups','user_permissions']
        if request.user.is_staff_member:
            self.add_fieldsets[0][1]['fields'] = ['email','password1','password2','username','ph','address','is_merchant','is_active','groups']
        return super().get_form(request, obj, **kwargs)
    
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = []


admin.site.register(User,UserAdmin)

