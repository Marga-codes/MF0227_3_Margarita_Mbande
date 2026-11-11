from django.test import TestCase
from django.urls import reverse

from .forms import IncidenciaForm
from .models import Incidencia, Tecnico


class IncidenciaModelTests(TestCase):
    def test_valores_por_defecto(self):
        inc = Incidencia.objects.create(titulo="Impresora atascada", descripcion="Atasco en bandeja 2")
        self.assertEqual(inc.estado, Incidencia.Estado.ABIERTO)
        self.assertEqual(inc.prioridad, Incidencia.Prioridad.MEDIA)
        self.assertIsNotNone(inc.fecha_creacion)

    def test_relacion_con_tecnico(self):
        tec = Tecnico.objects.create(nombre="Ana López", especialidad="Redes", email="ana@example.com")
        Incidencia.objects.create(titulo="Sin conexión WiFi", descripcion="Planta 3", tecnico=tec)
        self.assertEqual(tec.incidencias.count(), 1)

    def test_borrar_tecnico_conserva_incidencia(self):
        tec = Tecnico.objects.create(nombre="Luis Gil", especialidad="Hardware", email="luis@example.com")
        inc = Incidencia.objects.create(titulo="Teclado roto", descripcion="Tecla Enter", tecnico=tec)
        tec.delete()
        inc.refresh_from_db()
        self.assertIsNone(inc.tecnico)


class IncidenciaFormTests(TestCase):
    def test_campos_vacios_no_validan(self):
        form = IncidenciaForm(data={"titulo": "", "descripcion": "", "prioridad": "MEDIA"})
        self.assertFalse(form.is_valid())
        self.assertIn("titulo", form.errors)
        self.assertIn("descripcion", form.errors)

    def test_titulo_demasiado_corto(self):
        form = IncidenciaForm(data={"titulo": "abc", "descripcion": "algo", "prioridad": "MEDIA"})
        self.assertFalse(form.is_valid())
        self.assertIn("titulo", form.errors)


class IncidenciaViewTests(TestCase):
    def test_lista_responde_y_muestra_incidencias(self):
        Incidencia.objects.create(titulo="Pantalla azul", descripcion="BSOD al arrancar")
        resp = self.client.get(reverse("incidencias:lista"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "base.html")
        self.assertContains(resp, "Pantalla azul")

    def test_filtro_por_estado(self):
        Incidencia.objects.create(titulo="Abierta uno", descripcion="x")
        Incidencia.objects.create(titulo="Cerrada uno", descripcion="x", estado=Incidencia.Estado.CERRADO)
        resp = self.client.get(reverse("incidencias:lista"), {"estado": "CERRADO"})
        self.assertContains(resp, "Cerrada uno")
        self.assertNotContains(resp, "Abierta uno")

    def test_crear_incidencia_desde_formulario(self):
        tec = Tecnico.objects.create(nombre="Marta Ruiz", especialidad="Software", email="marta@example.com")
        resp = self.client.post(
            reverse("incidencias:nueva"),
            {"titulo": "Outlook no sincroniza", "descripcion": "Error 0x800", "prioridad": "ALTA", "tecnico": tec.pk},
            follow=True,
        )
        self.assertRedirects(resp, reverse("incidencias:lista"))
        self.assertContains(resp, "registrada correctamente")
        inc = Incidencia.objects.get()
        self.assertEqual(inc.tecnico, tec)
        self.assertEqual(inc.estado, Incidencia.Estado.ABIERTO)

    def test_post_invalido_no_crea_y_muestra_errores(self):
        resp = self.client.post(reverse("incidencias:nueva"), {"titulo": "", "descripcion": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Incidencia.objects.count(), 0)
        self.assertContains(resp, "obligatorio")
