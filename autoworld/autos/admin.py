from django.contrib import admin

from autos.models import *


class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'spare', 'time_create')
    list_display_links = ('id', 'spare')


class AutoAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'odo', 'owner')
    list_display_links = ('brand', 'model')


class SpareAdmin(admin.ModelAdmin):
    list_display = ('name', 'partnumber', 'manufacturer')
    list_display_links = ('name', 'partnumber', 'manufacturer')


admin.site.register(Auto, AutoAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Spare, SpareAdmin)
