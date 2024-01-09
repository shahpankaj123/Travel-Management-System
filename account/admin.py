from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email","name","ph","is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name","ph"]}),
        ("Permissions", {"fields": ["is_superuser","is_admin","is_active","is_merchant","is_staff_member","is_customer_user","groups","user_permissions"]}),
        ("Token_Verify",{"fields":["tc"]})
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name","ph" ,"password1", "password2","is_superuser","is_admin","is_active","is_merchant","is_staff_member","is_customer_user","groups","user_permissions"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = []


# Now register the new UserAdmin..
admin.site.register(User,UserAdmin)

