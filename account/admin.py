from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from bus_reserve import models

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

@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Bus
        fields = '__all__'

@admin.register(models.Route)
class RouteAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Route
        fields = '__all__'

@admin.register(models.BusSchedule)
class BusScheduleAdmin(admin.ModelAdmin):
    class Meta:
        model = models.BusSchedule
        fields = '__all__'

@admin.register(models.Seat)
class SeatAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Seat
        fields = '__all__'

@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Ticket
        fields = '__all__'

@admin.register(models.TicketOrder)
class TicketOrderAdmin(admin.ModelAdmin):
    class Meta:
        model = models.TicketOrder
        fields = '__all__'

@admin.register(models.TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    class Meta:
        model = models.TicketHistory
        fields = '__all__'

@admin.register(models.DepartInfo)
class DepartInfoAdmin(admin.ModelAdmin):
    class Meta:
        model = models.DepartInfo
        fields = '__all__'