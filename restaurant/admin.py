from django.contrib import admin

from restaurant.models import Table, Booking, ContentText, ContentImage


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "places",  "flour", "description",)
    list_filter = ("number",)
    search_fields = ("number", "description")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "table", "places", "notification", "date_field", "time_start", "time_end", "active", "created_at")
    list_filter = ("user", "table", "date_field", "time_start")
    search_fields = ("user", "table")

@admin.register(ContentImage)
class ContentImageAdmin(admin.ModelAdmin):
    list_display = ("title", "description",  "image",)
    list_filter = ("title",)
    search_fields = ("title", "description")

@admin.register(ContentText)
class ContentTextAdmin(admin.ModelAdmin):
    list_display = ("title", "body",)
    list_filter = ("title",)
    search_fields = ("title", "body",)

