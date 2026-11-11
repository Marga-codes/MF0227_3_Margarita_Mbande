from django.contrib import admin

from .models import Incidencia, Tecnico


class IncidenciaInline(admin.TabularInline):
    model = Incidencia
    fields = ("titulo", "estado", "prioridad")
    extra = 0
    show_change_link = True


@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "especialidad", "email", "num_incidencias")
    list_filter = ("especialidad",)
    search_fields = ("nombre", "email", "especialidad")
    inlines = [IncidenciaInline]

    @admin.display(description="nº incidencias")
    def num_incidencias(self, obj):
        return obj.incidencias.count()


@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "estado", "prioridad", "tecnico", "fecha_creacion")
    list_display_links = ("id", "titulo")
    list_filter = ("estado", "prioridad", "tecnico")
    search_fields = ("titulo", "descripcion", "tecnico__nombre")
    list_editable = ("estado",)
    list_select_related = ("tecnico",)
    date_hierarchy = "fecha_creacion"
    readonly_fields = ("fecha_creacion",)
