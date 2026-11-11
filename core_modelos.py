"""
core_modelos.py — Bloque 1 (UF2404): Principios de POO en Python.

Modelo de dominio independiente de Django para el HelpDesk:
- Encapsulamiento: atributos protegidos (_id, _titulo, _estado, _prioridad)
  expuestos mediante propiedades de solo lectura.
- Herencia: TicketHardware y TicketSoftware heredan de TicketTecnico.
- Polimorfismo: cada subclase sobrescribe calcular_sla().
- Excepciones personalizadas: EstadoInvalidoError, PrioridadInvalidaError.
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------- #
# Excepciones personalizadas
# --------------------------------------------------------------------------- #
class TicketError(Exception):
    """Excepción base del dominio de tickets."""


class EstadoInvalidoError(TicketError):
    """Se lanza al intentar una transición de estado no permitida."""


class PrioridadInvalidaError(TicketError):
    """Se lanza cuando la prioridad no es una de las admitidas."""


# --------------------------------------------------------------------------- #
# Clase base
# --------------------------------------------------------------------------- #
class TicketTecnico(ABC):
    """Ticket técnico genérico. No se instancia directamente (clase abstracta)."""

    ABIERTO = "Abierto"
    EN_PROCESO = "En Proceso"
    CERRADO = "Cerrado"
    ESTADOS = (ABIERTO, EN_PROCESO, CERRADO)

    PRIORIDADES = ("Baja", "Media", "Alta", "Critica")

    # Transiciones lógicas permitidas: estado_actual -> {estados_destino}
    # Un ticket cerrado solo puede reabrirse (volver a Abierto), nunca pasar
    # directamente a En Proceso.
    TRANSICIONES = {
        ABIERTO: {EN_PROCESO, CERRADO},
        EN_PROCESO: {ABIERTO, CERRADO},
        CERRADO: {ABIERTO},
    }

    def __init__(self, id_ticket: int, titulo: str, prioridad: str = "Media"):
        if not isinstance(id_ticket, int) or id_ticket <= 0:
            raise ValueError("El id debe ser un entero positivo.")
        if not titulo or not titulo.strip():
            raise ValueError("El título no puede estar vacío.")
        self._id = id_ticket
        self._titulo = titulo.strip()
        self._prioridad = self._validar_prioridad(prioridad)
        self._estado = self.ABIERTO

    # -- Propiedades (encapsulamiento) ------------------------------------- #
    @property
    def id(self) -> int:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def prioridad(self) -> str:
        return self._prioridad

    @prioridad.setter
    def prioridad(self, valor: str) -> None:
        self._prioridad = self._validar_prioridad(valor)

    # -- Validaciones internas --------------------------------------------- #
    @classmethod
    def _validar_prioridad(cls, prioridad: str) -> str:
        if prioridad not in cls.PRIORIDADES:
            raise PrioridadInvalidaError(
                f"Prioridad '{prioridad}' no válida. Usa una de: {', '.join(cls.PRIORIDADES)}."
            )
        return prioridad

    # -- Gestión de estados ------------------------------------------------ #
    def puede_cambiar_a(self, nuevo_estado: str) -> bool:
        return nuevo_estado in self.TRANSICIONES.get(self._estado, set())

    def cambiar_estado(self, nuevo_estado: str) -> None:
        """Cambia el estado validando que la transición sea lógica."""
        if nuevo_estado not in self.ESTADOS:
            raise EstadoInvalidoError(f"El estado '{nuevo_estado}' no existe.")
        if not self.puede_cambiar_a(nuevo_estado):
            raise EstadoInvalidoError(
                f"Transición no permitida: '{self._estado}' -> '{nuevo_estado}'."
            )
        self._estado = nuevo_estado

    # Atajos legibles
    def iniciar(self) -> None:
        self.cambiar_estado(self.EN_PROCESO)

    def cerrar(self) -> None:
        self.cambiar_estado(self.CERRADO)

    def reabrir(self) -> None:
        self.cambiar_estado(self.ABIERTO)

    # -- Polimorfismo ------------------------------------------------------ #
    @abstractmethod
    def calcular_sla(self) -> int:
        """Horas máximas de resolución según prioridad y tipo de ticket."""

    def tipo(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return (
            f"[{self.tipo()} #{self._id}] {self._titulo} | "
            f"estado={self._estado} | prioridad={self._prioridad} | "
            f"SLA={self.calcular_sla()}h"
        )

    def __repr__(self) -> str:
        return f"{self.tipo()}(id={self._id!r}, titulo={self._titulo!r})"


# --------------------------------------------------------------------------- #
# Clases hijas
# --------------------------------------------------------------------------- #
class TicketHardware(TicketTecnico):
    """Incidencia física: requiere desplazamiento o piezas, SLA más amplio."""

    SLA_HORAS = {"Baja": 72, "Media": 48, "Alta": 24, "Critica": 8}

    def __init__(self, id_ticket: int, titulo: str, componente: str, prioridad: str = "Media"):
        super().__init__(id_ticket, titulo, prioridad)
        if not componente or not componente.strip():
            raise ValueError("El componente no puede estar vacío.")
        self._componente = componente.strip()

    @property
    def componente(self) -> str:
        return self._componente

    def calcular_sla(self) -> int:
        return self.SLA_HORAS[self._prioridad]

    def __str__(self) -> str:
        return f"{super().__str__()} | componente={self._componente}"


class TicketSoftware(TicketTecnico):
    """Incidencia lógica: se resuelve en remoto, SLA más corto."""

    SLA_HORAS = {"Baja": 48, "Media": 24, "Alta": 8, "Critica": 4}

    def __init__(self, id_ticket: int, titulo: str, sistema_operativo: str, prioridad: str = "Media"):
        super().__init__(id_ticket, titulo, prioridad)
        if not sistema_operativo or not sistema_operativo.strip():
            raise ValueError("El sistema operativo no puede estar vacío.")
        self._sistema_operativo = sistema_operativo.strip()

    @property
    def sistema_operativo(self) -> str:
        return self._sistema_operativo

    def calcular_sla(self) -> int:
        horas = self.SLA_HORAS[self._prioridad]
        # Los sistemas heredados no tienen soporte del fabricante: +50 %.
        if "xp" in self._sistema_operativo.lower():
            horas = int(horas * 1.5)
        return horas

    def __str__(self) -> str:
        return f"{super().__str__()} | SO={self._sistema_operativo}"


# --------------------------------------------------------------------------- #
# Pruebas unitarias básicas / demostración
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    superadas = 0
    total = 0

    def comprobar(descripcion: str, condicion: bool) -> None:
        global superadas, total
        total += 1
        superadas += int(condicion)
        print(f"  [{'OK ' if condicion else 'ERR'}] {descripcion}")

    print("1) Creación de instancias y polimorfismo")
    tickets = [
        TicketHardware(1, "Pantalla no enciende", componente="Monitor", prioridad="Alta"),
        TicketSoftware(2, "Error al iniciar Outlook", sistema_operativo="Windows 11", prioridad="Alta"),
        TicketSoftware(3, "Aplicación antigua", sistema_operativo="Windows XP", prioridad="Media"),
    ]
    for t in tickets:
        print("   ", t)
    comprobar("Hardware Alta -> 24h", tickets[0].calcular_sla() == 24)
    comprobar("Software Alta -> 8h", tickets[1].calcular_sla() == 8)
    comprobar("Software Media en XP -> 36h", tickets[2].calcular_sla() == 36)

    print("\n2) Transiciones de estado válidas")
    t = tickets[0]
    t.iniciar()
    comprobar("Abierto -> En Proceso", t.estado == "En Proceso")
    t.cerrar()
    comprobar("En Proceso -> Cerrado", t.estado == "Cerrado")

    print("\n3) Transición no permitida: Cerrado -> En Proceso")
    try:
        t.iniciar()
        comprobar("Debe lanzar EstadoInvalidoError", False)
    except EstadoInvalidoError as e:
        print("    Capturada:", e)
        comprobar("Lanza EstadoInvalidoError y conserva el estado", t.estado == "Cerrado")

    print("\n4) Reapertura permitida: Cerrado -> Abierto")
    t.reabrir()
    comprobar("Cerrado -> Abierto", t.estado == "Abierto")

    print("\n5) Estado inexistente")
    try:
        t.cambiar_estado("Pendiente")
        comprobar("Debe lanzar EstadoInvalidoError", False)
    except EstadoInvalidoError as e:
        print("    Capturada:", e)
        comprobar("Rechaza estados inexistentes", True)

    print("\n6) Prioridad inválida")
    try:
        TicketSoftware(4, "Prueba", sistema_operativo="Linux", prioridad="Urgentísima")
        comprobar("Debe lanzar PrioridadInvalidaError", False)
    except PrioridadInvalidaError as e:
        print("    Capturada:", e)
        comprobar("Rechaza prioridades no admitidas", True)

    print("\n7) Encapsulamiento")
    try:
        t.estado = "Cerrado"  # propiedad sin setter
        comprobar("No debe poder asignarse el estado directamente", False)
    except AttributeError:
        comprobar("El estado solo cambia mediante cambiar_estado()", t.estado == "Abierto")

    print("\n8) Clase abstracta")
    try:
        TicketTecnico(5, "Genérico")
        comprobar("No debe poder instanciarse TicketTecnico", False)
    except TypeError:
        comprobar("TicketTecnico no es instanciable", True)

    print(f"\nResultado: {superadas}/{total} comprobaciones superadas.")
    raise SystemExit(0 if superadas == total else 1)
