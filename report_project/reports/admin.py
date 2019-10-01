from django.contrib import admin
from .models import Event, Informe, SatImage, Area, Location

# Register your models here.

admin.site.register(Event)
# admin.site.register(Informe)  ## Informe should be created using the custom app

admin.site.register(Area)
admin.site.register(Location)


class InformeAdmin(admin.ModelAdmin):
    list_display = ['informe_code', 'title', 'fecha', 'event', 'satimage1', 'satimage2' ]
admin.site.register(Informe, InformeAdmin)


class SatImageAdmin(admin.ModelAdmin):
    list_display = ['event', 'fuente', 'banda', 'fecha', 'image']
admin.site.register(SatImage, SatImageAdmin)


