from django.contrib import admin

# Register your models here.
from charts.models import chart
class chartAdmin(admin.ModelAdmin):
    search_fields = (['title'])
admin.site.register(chart,chartAdmin)
