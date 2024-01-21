from django.contrib import admin
from . import models

# Register your models here.
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

# @admin.register(models.Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     class Meta:
#         model = models.Ticket
#         fields = '__all__'

# @admin.register(models.TicketOrder)
# class TicketOrderAdmin(admin.ModelAdmin):
#     class Meta:
#         model = models.TicketOrder
#         fields = '__all__'

@admin.register(models.TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    class Meta:
        model = models.TicketHistory
        fields = '__all__'

# @admin.register(models.DepartInfo)
# class DepartInfoAdmin(admin.ModelAdmin):
#     class Meta:
#         model = models.DepartInfo
#         fields = '__all__'