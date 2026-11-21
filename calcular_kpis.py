#!/usr/bin/env python3
"""
=============================================================================
PUKLLAY SPORT - MOTOR DE CÁLCULO DE KPIS Y ANALÍTICA (PYTHON 3)
=============================================================================
Calcula métricas clave del sistema:
1. Ingresos totales mensuales (Facturación vs Adelantos del 50%)
2. Porcentaje de ocupación de canchas vs capacidad máxima (450 horas/mes)
3. Distribución territorial de reservas por sede y distrito
=============================================================================
"""

import sys
import json
from backend_poo import PukllayService, MotorAnaliticaKPIs


def main():
    service = PukllayService()
    anio = 2026
    formato_json = "--json" in sys.argv

    kpis = service.obtener_kpis_dashboard(anio=anio)

    if formato_json:
        print(json.dumps(kpis, indent=2, ensure_ascii=False))
        return

    resumen = kpis["resumen"]
    print("=" * 72)
    print(" 📊 PUKLLAY SPORT - DASHBOARD EJECUTIVO DE KPIS & MÉTRICAS (PYTHON)")
    print("=" * 72)
    print(f" • Año evaluado:                 {kpis['anio']}")
    print(f" • Facturación Total Anual:      S/. {resumen['totalIngresosAnual']:,.2f}")
    print(f" • Tasa Promedio de Ocupación:   {resumen['promedioOcupacionGlobal']}%")
    print(f" • Total de Reservas Registradas:{resumen['totalReservasHistoricas']}")
    print(f" • Complejo Deportivo Líder:     {resumen['sedeLider']}")
    print("-" * 72)

    print("\n1. FACTURACIÓN MENSUAL (EN SOLES):")
    print(f" {'Mes':<6} | {'Facturación':<14} | {'Adelantos (50%)':<16} | {'Reservas':<8}")
    print("-" * 52)
    for m in kpis["ingresosPorMes"]:
        print(f" {m['nombre']:<6} | S/. {m['ingresos']:<10,.2f} | S/. {m['adelantos']:<12,.2f} | {m['reservas']:<8}")

    print("\n2. ÍNDICE DE OCUPACIÓN POR CANCHA DE GRASS:")
    print(f" {'Cancha':<30} | {'Sede':<24} | {'Ocupación':<10} | {'Horas':<8}")
    print("-" * 78)
    for c in kpis["ocupacionCanchas"]:
        barra = "█" * int(c["ocupacion"] / 10) + "░" * (10 - int(c["ocupacion"] / 10))
        print(f" {c['nombre'][:28]:<30} | {c['sede'][:22]:<24} | {barra} {c['ocupacion']:>5}% | {c['horasOcupadas']}/{c['horasDisponibles']}h")

    print("\n3. DISTRIBUCIÓN TERRITORIAL POR SEDE:")
    print(f" {'Complejo Deportivo':<32} | {'Distrito':<18} | {'Reservas':<10} | {'Recaudado':<14}")
    print("-" * 80)
    for s in kpis["distribucionSedes"]:
        print(f" {s['nombre'][:30]:<32} | {s['distrito']:<18} | {s['reservasTotales']:<10} | S/. {s['recaudado']:<10,.2f}")

    print("\n" + "=" * 72)
    print(" ✅ Cálculo analítico completado exitosamente con Python 3.")
    print("=" * 72)


if __name__ == "__main__":
    main()
