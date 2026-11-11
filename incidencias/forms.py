from django import forms

from .models import Incidencia


class IncidenciaForm(forms.ModelForm):
    """Formulario para registrar una nueva incidencia desde la web."""

    class Meta:
        model = Incidencia
        fields = ["titulo", "descripcion", "prioridad", "tecnico"]
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Ej.: El portátil no arranca"}),
            "descripcion": forms.Textarea(attrs={"rows": 5, "placeholder": "Describe el problema"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tecnico"].empty_label = "Sin asignar"
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs["class"] = css

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if len(titulo) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return titulo

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()
        if not descripcion:
            raise forms.ValidationError("La descripción no puede estar vacía.")
        return descripcion
