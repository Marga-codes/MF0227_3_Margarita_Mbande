"""Rutas principales de helpdesk_project."""
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "HelpDesk · Administración"
admin.site.site_title = "HelpDesk"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("incidencias.urls")),
]
