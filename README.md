# HelpDesk · Sistema de Gestión de Incidencias Técnicas

Prueba práctica del módulo **MF0227_3 – Programación orientada a objetos**
(certificado IFCD0112). Autora: Margarita Mbande.

Aplicación web en Django para registrar y consultar incidencias técnicas y
asignarlas a técnicos, junto con un módulo de dominio en Python puro que aplica
los principios de la POO.

## Requisitos

- Python 3.10 o superior
- Git

## Instalación y despliegue local

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd MF0227_3_Margarita_Mbande

# 2. Crear y activar el entorno virtual
python -m venv venv
source venv/bin/activate          # Linux / macOS
venv\Scripts\activate             # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Crear un usuario para el panel de administración
python manage.py createsuperuser

# 6. Levantar el servidor
python manage.py runserver
```

| URL | Contenido |
|-----|-----------|
| http://127.0.0.1:8000/ | Lista de incidencias (filtrable por estado) |
| http://127.0.0.1:8000/nueva/ | Formulario para registrar una incidencia |
| http://127.0.0.1:8000/admin/ | Panel de administración |

### Pruebas

```bash
python core_modelos.py            # Bloque 1: demostración y pruebas de POO
python manage.py test incidencias # Bloque 2: pruebas automáticas de Django
```

### Variables de entorno (opcionales)

| Variable | Uso | Valor por defecto |
|----------|-----|-------------------|
| `DJANGO_SECRET_KEY` | Clave secreta de Django | Clave de desarrollo |
| `DJANGO_DEBUG` | `1` activa el modo depuración, `0` lo desactiva | `1` |

## Estructura del proyecto

```
MF0227_3_Margarita_Mbande/
├── core_modelos.py            # Bloque 1 · POO en Python puro
├── manage.py
├── requirements.txt
├── helpdesk_project/          # Configuración del proyecto Django
│   ├── settings.py
│   └── urls.py
├── incidencias/               # App Django
│   ├── models.py              # Tecnico, Incidencia
│   ├── admin.py               # Panel de administración
│   ├── forms.py               # IncidenciaForm
│   ├── views.py               # ListView y CreateView
│   ├── urls.py
│   ├── tests.py
│   ├── migrations/
│   └── templates/incidencias/
│       ├── incidencia_list.html
│       └── incidencia_form.html
├── templates/base.html        # Plantilla base (Bootstrap 5)
├── pruebas.txt                # Plan de pruebas
└── empaquetar.sh              # Genera el .zip de entrega
```

## Arquitectura: cómo se relacionan las UF

**UF2404 · POO (`core_modelos.py`).** Modela el dominio sin depender de ningún
framework. `TicketTecnico` es una clase base abstracta con atributos protegidos
(`_id`, `_titulo`, `_estado`, `_prioridad`) que solo se leen mediante
propiedades. El estado solo cambia con `cambiar_estado()`, que valida las
transiciones:

```
Abierto ──► En Proceso ──► Cerrado
   ▲            │            │
   └────────────┘            │
   ▲                         │
   └──────── (reabrir) ──────┘     Cerrado ──► En Proceso: EstadoInvalidoError
```

`TicketHardware` (con `componente`) y `TicketSoftware` (con
`sistema_operativo`) heredan de ella y sobrescriben `calcular_sla()`
(polimorfismo). Los errores se notifican con excepciones propias
(`EstadoInvalidoError`, `PrioridadInvalidaError`).

**UF2405 · Web y base de datos (`helpdesk_project` + `incidencias`).** Lleva el
mismo dominio a una aplicación web con el patrón MVT de Django:

- **Modelo:** `Tecnico` 1 ── N `Incidencia` mediante `ForeignKey`
  (`on_delete=SET_NULL`, para no perder el histórico si se da de baja a un
  técnico). Estado y prioridad usan `TextChoices`, con los mismos valores que en
  el Bloque 1. El ORM persiste los datos en SQLite.
- **Vista:** `IncidenciaListView` (lista, filtro por estado, paginación) e
  `IncidenciaCreateView` (alta mediante `IncidenciaForm`, que valida campos
  vacíos y la longitud mínima del título).
- **Plantilla:** `base.html` define el diseño común con Bootstrap 5 y las
  plantillas de lista y formulario la extienden.
- **Admin:** permite gestionar técnicos e incidencias con `list_display`, filtros
  por estado, prioridad y técnico, y búsqueda por título o nombre del técnico.

**UF2406 · Ciclo de vida.** El desarrollo sigue las fases de análisis
(enunciado), diseño (dominio POO), implementación (Django), pruebas
(`core_modelos.py`, `tests.py` y `pruebas.txt`) y entrega (`empaquetar.sh`).
El control de versiones usa dos ramas:

- `desarrollo`: rama de trabajo, con un commit atómico por funcionalidad
  (POO → proyecto → modelos → admin → vistas y plantillas → pruebas → documentación).
- `main`: rama estable, que recibe `desarrollo` mediante merge al cerrar la entrega.

## Plan de pruebas

Los casos de prueba funcionales ejecutados están en [`pruebas.txt`](pruebas.txt).

## Entrega

```bash
./empaquetar.sh   # genera MF0227_3_Margarita_Mbande.zip sin venv ni __pycache__
```
