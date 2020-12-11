from django.contrib import admin
from .models import ManagementCommand


@admin.register(ManagementCommand)
class ManagementCommandsAdmin(admin.ModelAdmin):
    list_display = ("app", "name", "expose")
    list_filter = ("app",)
    list_editable = ("expose",)
    list_per_page = 20

    ordering = ("app", "name", "expose")
    search_fields = ("app", "name",)
    readonly_fields = ("app", "name",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
