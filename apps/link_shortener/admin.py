from django.contrib import admin

from .models import ShortLink

@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ("alias", "url", "clicks", "is_active", "created_at", "expires_at")
    list_filter = ("is_active", "created_at", "expires_at")
    search_fields = ("alias", "url")
    readonly_fields = ("created_at", "updated_at", "clicks")
    list_editable = ("is_active",)
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()

