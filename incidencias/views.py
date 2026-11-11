from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import IncidenciaForm
from .models import Incidencia


class IncidenciaListView(ListView):
    """Lista todas las incidencias, con filtro opcional por estado (?estado=ABIERTO)."""

    model = Incidencia
    template_name = "incidencias/incidencia_list.html"
    context_object_name = "incidencias"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("tecnico")
        estado = self.request.GET.get("estado")
        if estado in Incidencia.Estado.values:
            qs = qs.filter(estado=estado)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estados"] = Incidencia.Estado.choices
        context["estado_actual"] = self.request.GET.get("estado", "")
        return context


class IncidenciaCreateView(CreateView):
    """Registra una nueva incidencia. Siempre se crea en estado Abierto."""

    model = Incidencia
    form_class = IncidenciaForm
    template_name = "incidencias/incidencia_form.html"
    success_url = reverse_lazy("incidencias:lista")

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        messages.success(self.request, f"Incidencia {self.object} registrada correctamente.")
        return respuesta
