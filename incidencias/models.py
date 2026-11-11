from django.db import models
from django.urls import reverse


class Tecnico(models.Model):
    """Técnico del equipo de soporte que puede tener incidencias asignadas."""

    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "técnico"
        verbose_name_plural = "técnicos"

    def __str__(self):
        return f"{self.nombre} ({self.especialidad})"


class Incidencia(models.Model):
    """Incidencia técnica registrada en el HelpDesk."""

    class Estado(models.TextChoices):
        ABIERTO = "ABIERTO", "Abierto"
        EN_PROCESO = "EN_PROCESO", "En Proceso"
        CERRADO = "CERRADO", "Cerrado"

    class Prioridad(models.TextChoices):
        BAJA = "BAJA", "Baja"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"
        CRITICA = "CRITICA", "Crítica"

    titulo = models.CharField("título", max_length=150)
    descripcion = models.TextField("descripción")
    fecha_creacion = models.DateTimeField("fecha de creación", auto_now_add=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ABIERTO)
    prioridad = models.CharField(max_length=20, choices=Prioridad.choices, default=Prioridad.MEDIA)
    # ForeignKey: un técnico puede tener muchas incidencias asignadas.
    # SET_NULL para no perder el histórico si se da de baja a un técnico.
    tecnico = models.ForeignKey(
        Tecnico,
        verbose_name="técnico asignado",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incidencias",
    )

    class Meta:
        ordering = ["-fecha_creacion"]
        verbose_name = "incidencia"
        verbose_name_plural = "incidencias"

    def __str__(self):
        return f"#{self.pk} {self.titulo}"

    def get_absolute_url(self):
        return reverse("incidencias:lista")
