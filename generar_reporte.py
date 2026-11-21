#!/usr/bin/env python3
"""
=============================================================================
PUKLLAY SPORT - GENERADOR OFICIAL DE REPORTE FORMAL AUDITABLE (PYTHON 3)
=============================================================================
Genera un informe detallado e inmutable del estado del sistema, facturación,
reservas, atenciones y controles de seguridad para la administración.
=============================================================================
"""

import sys
import json
from datetime import datetime
from backend_poo import PukllayService, GeneradorReporteFormal


def main():
    service = PukllayService()
    formato_json = "--json" in sys.argv
    reporte = service.generar_reporte_formal()

    if formato_json:
        print(json.dumps(reporte, indent=2, ensure_ascii=False))
        return

    stats = reporte["estadisticasGenerales"]
    auditor = reporte["auditor"]
    seguridad = reporte["cumplimientoSeguridad"]

    print("=" * 76)
    print(" 📄 INFORME FORMAL Y AUDITABLE DE GESTIÓN DEPORTIVA - PUKLLAY SPORT")
    print("=" * 76)
    print(f" Código de Auditoría:  {reporte['codigo']}")
    print(f" Fecha de Emisión:     {reporte['fechaGeneracion']}")
    print(f" Auditor Responsable:  {auditor['nombre']} ({auditor['email']})")
    print(f" Rol de Autoridad:     {auditor['rol']}")
    print("-" * 76)

    print("\n1. RESUMEN EJECUTIVO Y FINANCIERO:")
    print(f" • Facturación Global Estimada:       S/. {stats['facturacionTotal']:,.2f}")
    print(f" • Adelantos del 50% Recaudados:      S/. {stats['adelantosRecaudados']:,.2f}")
    print(f" • Saldos Pendientes a Cobrar:        S/. {stats['saldosPendientes']:,.2f}")
    print(f" • Total de Reservas en Historial:    {stats['totalReservas']}")
    print(f" • Complejos de Grass Registrados:    {stats['totalSedes']}")
    print(f" • Canchas Deportivas Habilitadas:    {stats['totalCanchas']}")
    print(f" • Usuarios en Plataforma:            {stats['totalUsuarios']}")

    print("\n2. PROTOCOLOS DE SEGURIDAD Y COMPLIMIENTO ANTIFRAUDE:")
    print(f" • Prevención de Fraude (KYC):        {seguridad['antifraudeKyc']}")
    print(f" • Bloqueo de Concurrencia:           {seguridad['bloqueoConcurrencia']}")
    print(f" • Trazabilidad e Integridad de Logs: {seguridad['auditoriaLogs']}")
    print(f" • Regla de Cancelación / Reembolso:  {seguridad['politicaCancelacion']}")

    print("\n3. DETALLE DE USUARIOS REGISTRADOS Y ROLES:")
    print(f" {'ID':<10} | {'Nombre':<24} | {'Email':<26} | {'Rol':<14}")
    print("-" * 76)
    for u in service.obtener_todos_usuarios():
        print(f" {u.id:<10} | {u.nombre[:22]:<24} | {u.email[:24]:<26} | {u.rol.value:<14}")

    print("\n4. SEDES Y CANCHAS BAJO GESTIÓN:")
    for s in service.obtener_sedes():
        check = "✓ VERIFICADA" if s.check_verificado_admin else "⏳ PENDIENTE"
        print(f" • [{s.id}] {s.nombre} ({s.distrito}) - Estado: {check}")
        for c in s.canchas:
            print(f"     -> {c.nombre} ({c.deporte.value}) | Tarifa: S/. {c.precio_base_hora:.2f}/h")

    print("\n" + "=" * 76)
    print(f" FIRMA DIGITAL: [PUKLLAY-SHA256-AUDIT-{reporte['codigo']}]")
    print(" Reporte formal emitido conforme a las políticas vigentes de Pukllay Sport.")
    print("=" * 76)


if __name__ == "__main__":
    main()
